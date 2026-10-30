package com.helpdesk.service;

import com.helpdesk.dto.StatusUpdateRequest;
import com.helpdesk.dto.TicketCreateRequest;
import com.helpdesk.entity.Category;
import com.helpdesk.entity.SlaPolicy;
import com.helpdesk.entity.Ticket;
import com.helpdesk.entity.User;
import com.helpdesk.entity.enums.Priority;
import com.helpdesk.entity.enums.TicketStatus;
import com.helpdesk.repository.CategoryRepository;
import com.helpdesk.repository.SlaPolicyRepository;
import com.helpdesk.repository.TicketRepository;
import com.helpdesk.repository.UserRepository;
import jakarta.persistence.criteria.Predicate;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class TicketService {

    private final TicketRepository ticketRepository;
    private final CategoryRepository categoryRepository;
    private final UserRepository userRepository;
    private final SlaPolicyRepository slaPolicyRepository;

    /**
     * Lấy danh sách ticket với các bộ lọc động và kiểm tra trạng thái quá hạn
     */
    public List<Ticket> getAllTickets(TicketStatus status, Priority priority, String search, Long requesterId) {
        Specification<Ticket> spec = (root, query, cb) -> {
            List<Predicate> predicates = new ArrayList<>();

            if (status != null) {
                predicates.add(cb.equal(root.get("status"), status));
            }

            if (priority != null) {
                predicates.add(cb.equal(root.get("priority"), priority));
            }

            if (requesterId != null) {
                predicates.add(cb.equal(root.get("requester").get("id"), requesterId));
            }

            if (search != null && !search.trim().isEmpty()) {
                String searchPattern = "%" + search.trim().toLowerCase() + "%";
                Predicate codePredicate = cb.like(cb.lower(root.get("ticketCode")), searchPattern);
                Predicate titlePredicate = cb.like(cb.lower(root.get("title")), searchPattern);
                Predicate descPredicate = cb.like(cb.lower(root.get("description")), searchPattern);
                predicates.add(cb.or(codePredicate, titlePredicate, descPredicate));
            }

            return cb.and(predicates.toArray(new Predicate[0]));
        };

        List<Ticket> tickets = ticketRepository.findAll(spec, Sort.by(Sort.Direction.DESC, "id"));
        tickets.forEach(Ticket::checkOverdue);
        return tickets;
    }

    public Optional<Ticket> getTicketById(Long id) {
        Optional<Ticket> ticketOpt = ticketRepository.findById(id);
        ticketOpt.ifPresent(Ticket::checkOverdue);
        return ticketOpt;
    }

    public Optional<Ticket> getTicketByCode(String code) {
        Optional<Ticket> ticketOpt = ticketRepository.findByTicketCode(code);
        ticketOpt.ifPresent(Ticket::checkOverdue);
        return ticketOpt;
    }

    /**
     * Tạo mới Ticket: Tự động tính hạn giải quyết (dueDate) từ SLA Policy và sinh mã TicketCode
     */
    @Transactional
    public Ticket createTicket(TicketCreateRequest req) {
        Category category = categoryRepository.findById(req.getCategoryId())
                .orElseThrow(() -> new IllegalArgumentException("Không tìm thấy danh mục với ID: " + req.getCategoryId()));

        User requester = userRepository.findById(req.getRequesterId())
                .orElseThrow(() -> new IllegalArgumentException("Không tìm thấy người yêu cầu với ID: " + req.getRequesterId()));

        Priority priority = req.getPriority() != null ? req.getPriority() : Priority.MEDIUM;

        // Tìm thời gian SLA cam kết
        int resolutionHours = slaPolicyRepository.findByPriorityLevel(priority)
                .map(SlaPolicy::getResolutionTimeHours)
                .orElse(24);

        LocalDateTime now = LocalDateTime.now();
        LocalDateTime dueDate = now.plusHours(resolutionHours);

        // Sinh mã TicketCode duy nhất (VD: TK-1006)
        long count = ticketRepository.count();
        String ticketCode = generateTicketCode(count + 1);

        Ticket ticket = Ticket.builder()
                .ticketCode(ticketCode)
                .title(req.getTitle())
                .description(req.getDescription())
                .status(TicketStatus.OPEN)
                .priority(priority)
                .category(category)
                .requester(requester)
                .assignee(null)
                .createdAt(now)
                .dueDate(dueDate)
                .isOverdue(false)
                .build();

        return ticketRepository.save(ticket);
    }

    /**
     * Cập nhật trạng thái và kỹ thuật viên tiếp nhận
     */
    @Transactional
    public Ticket updateStatus(Long id, StatusUpdateRequest req) {
        Ticket ticket = ticketRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Không tìm thấy Ticket với ID: " + id));

        if (req.getStatus() != null) {
            ticket.setStatus(req.getStatus());
        }

        if (req.getAssigneeId() != null) {
            User assignee = userRepository.findById(req.getAssigneeId())
                    .orElseThrow(() -> new IllegalArgumentException("Không tìm thấy Kỹ thuật viên với ID: " + req.getAssigneeId()));
            ticket.setAssignee(assignee);
        }

        ticket.checkOverdue();
        return ticketRepository.save(ticket);
    }

    @Transactional
    public Ticket saveTicket(Ticket ticket) {
        ticket.checkOverdue();
        return ticketRepository.save(ticket);
    }

    private String generateTicketCode(long seed) {
        String code = String.format("TK-%04d", seed);
        int attempts = 0;
        while (ticketRepository.findByTicketCode(code).isPresent()) {
            attempts++;
            code = String.format("TK-%04d", seed + attempts);
        }
        return code;
    }
}
