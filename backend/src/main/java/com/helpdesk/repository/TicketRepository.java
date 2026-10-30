package com.helpdesk.repository;

import com.helpdesk.entity.Ticket;
import com.helpdesk.entity.enums.TicketStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface TicketRepository extends JpaRepository<Ticket, Long>, JpaSpecificationExecutor<Ticket> {
    Optional<Ticket> findByTicketCode(String ticketCode);
    List<Ticket> findByStatus(TicketStatus status);
    List<Ticket> findByRequesterId(Long requesterId);
    List<Ticket> findByAssigneeId(Long assigneeId);
}
