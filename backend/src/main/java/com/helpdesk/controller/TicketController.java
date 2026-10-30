package com.helpdesk.controller;

import com.helpdesk.dto.CommentCreateRequest;
import com.helpdesk.dto.StatusUpdateRequest;
import com.helpdesk.dto.TicketCreateRequest;
import com.helpdesk.entity.Ticket;
import com.helpdesk.entity.TicketComment;
import com.helpdesk.entity.enums.Priority;
import com.helpdesk.entity.enums.TicketStatus;
import com.helpdesk.service.CommentService;
import com.helpdesk.service.TicketService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/tickets")
@RequiredArgsConstructor
public class TicketController {

    private final TicketService ticketService;
    private final CommentService commentService;

    /**
     * Lấy danh sách Ticket có bộ lọc động
     */
    @GetMapping
    public ResponseEntity<List<Ticket>> getAllTickets(
            @RequestParam(required = false) TicketStatus status,
            @RequestParam(required = false) Priority priority,
            @RequestParam(required = false) String search,
            @RequestParam(required = false) Long requesterId
    ) {
        return ResponseEntity.ok(ticketService.getAllTickets(status, priority, search, requesterId));
    }

    /**
     * Lấy chi tiết Ticket theo ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<Ticket> getTicketById(@PathVariable Long id) {
        return ticketService.getTicketById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Tạo Ticket mới (Tự động tính SLA dueDate & mã Ticket)
     */
    @PostMapping
    public ResponseEntity<Ticket> createTicket(@RequestBody TicketCreateRequest req) {
        Ticket createdTicket = ticketService.createTicket(req);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdTicket);
    }

    /**
     * Cập nhật trạng thái và kỹ thuật viên tiếp nhận
     */
    @PatchMapping("/{id}/status")
    public ResponseEntity<Ticket> updateTicketStatus(
            @PathVariable Long id,
            @RequestBody StatusUpdateRequest req
    ) {
        Ticket updatedTicket = ticketService.updateStatus(id, req);
        return ResponseEntity.ok(updatedTicket);
    }

    /**
     * Lấy danh sách bình luận của Ticket
     */
    @GetMapping("/{id}/comments")
    public ResponseEntity<List<TicketComment>> getTicketComments(@PathVariable Long id) {
        return ResponseEntity.ok(commentService.getCommentsByTicketId(id));
    }

    /**
     * Thêm bình luận trao đổi mới vào Ticket
     */
    @PostMapping("/{id}/comments")
    public ResponseEntity<TicketComment> addComment(
            @PathVariable Long id,
            @RequestBody CommentCreateRequest req
    ) {
        TicketComment comment = commentService.addComment(id, req);
        return ResponseEntity.status(HttpStatus.CREATED).body(comment);
    }
}
