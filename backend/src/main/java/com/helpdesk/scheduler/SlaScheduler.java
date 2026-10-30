package com.helpdesk.scheduler;

import com.helpdesk.entity.Ticket;
import com.helpdesk.entity.enums.TicketStatus;
import com.helpdesk.repository.TicketRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Component
@Slf4j
@RequiredArgsConstructor
public class SlaScheduler {

    private final TicketRepository ticketRepository;

    /**
     * Tác vụ quét ngầm kiểm tra vi phạm thời hạn giải quyết sự cố (SLA Breach Scanner)
     * Tự động kích hoạt mỗi 60 giây một lần (fixedRate = 60000ms)
     */
    @Scheduled(fixedRate = 60000)
    @Transactional
    public void scanOverdueTickets() {
        LocalDateTime now = LocalDateTime.now();

        // Lấy tất cả các ticket đang mở hoặc đang xử lý
        List<Ticket> activeTickets = ticketRepository.findAll().stream()
                .filter(t -> t.getStatus() == TicketStatus.OPEN || t.getStatus() == TicketStatus.IN_PROGRESS)
                .toList();

        int newlyOverdueCount = 0;
        int totalOverdueCount = 0;

        for (Ticket ticket : activeTickets) {
            if (ticket.getDueDate() != null && now.isAfter(ticket.getDueDate())) {
                totalOverdueCount++;

                // Nếu trước đó chưa được đánh dấu là quá hạn
                if (!Boolean.TRUE.equals(ticket.getIsOverdue())) {
                    ticket.setIsOverdue(true);
                    ticketRepository.save(ticket);
                    newlyOverdueCount++;

                    log.warn("🚨 [CANH BAO VI PHAM SLA] Phieu ho tro [{}] - '{}' da qua han xu ly! Han cam ket: {}",
                            ticket.getTicketCode(),
                            ticket.getTitle(),
                            ticket.getDueDate());
                }
            }
        }

        log.info("⏱️ [SLA Scanner Daemon] Quet dinh ky hoan tat: Dang xu ly={} phieu, Tong so vi pham SLA={} phieu (Cap nhat moi={} phieu).",
                activeTickets.size(),
                totalOverdueCount,
                newlyOverdueCount);
    }
}
