package com.helpdesk.service;

import com.helpdesk.dto.DashboardStatsResponse;
import com.helpdesk.entity.Category;
import com.helpdesk.entity.Ticket;
import com.helpdesk.entity.enums.TicketStatus;
import com.helpdesk.repository.CategoryRepository;
import com.helpdesk.repository.TicketRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class DashboardService {

    private final TicketRepository ticketRepository;
    private final CategoryRepository categoryRepository;

    public DashboardStatsResponse getDashboardStats() {
        List<Ticket> allTickets = ticketRepository.findAll();
        LocalDateTime now = LocalDateTime.now();

        long totalTickets = allTickets.size();
        long openCount = 0;
        long inProgressCount = 0;
        long resolvedCount = 0;
        long closedCount = 0;
        long overdueCount = 0;

        Map<String, Long> categoryCountMap = new HashMap<>();
        List<Category> allCategories = categoryRepository.findAll();
        for (Category cat : allCategories) {
            categoryCountMap.put(cat.getName(), 0L);
        }

        for (Ticket ticket : allTickets) {
            // Đếm theo trạng thái
            if (ticket.getStatus() == TicketStatus.OPEN) {
                openCount++;
            } else if (ticket.getStatus() == TicketStatus.IN_PROGRESS) {
                inProgressCount++;
            } else if (ticket.getStatus() == TicketStatus.RESOLVED) {
                resolvedCount++;
            } else if (ticket.getStatus() == TicketStatus.CLOSED) {
                closedCount++;
            }

            // Đếm số lượng quá hạn
            boolean isOverdue = Boolean.TRUE.equals(ticket.getIsOverdue()) ||
                    (ticket.getDueDate() != null &&
                            ticket.getStatus() != TicketStatus.RESOLVED &&
                            ticket.getStatus() != TicketStatus.CLOSED &&
                            now.isAfter(ticket.getDueDate()));

            if (isOverdue) {
                overdueCount++;
            }

            // Đếm theo danh mục
            if (ticket.getCategory() != null) {
                String catName = ticket.getCategory().getName();
                categoryCountMap.put(catName, categoryCountMap.getOrDefault(catName, 0L) + 1);
            }
        }

        List<DashboardStatsResponse.StatusMetric> statusMetrics = List.of(
                DashboardStatsResponse.StatusMetric.builder().status("OPEN").label("Mới tiếp nhận").count(openCount).build(),
                DashboardStatsResponse.StatusMetric.builder().status("IN_PROGRESS").label("Đang xử lý").count(inProgressCount).build(),
                DashboardStatsResponse.StatusMetric.builder().status("RESOLVED").label("Đã giải quyết").count(resolvedCount).build(),
                DashboardStatsResponse.StatusMetric.builder().status("CLOSED").label("Đã đóng").count(closedCount).build()
        );

        List<DashboardStatsResponse.CategoryMetric> categoryMetrics = categoryCountMap.entrySet().stream()
                .map(entry -> DashboardStatsResponse.CategoryMetric.builder()
                        .categoryName(entry.getKey())
                        .count(entry.getValue())
                        .build())
                .sorted(Comparator.comparing(DashboardStatsResponse.CategoryMetric::getCategoryName))
                .collect(Collectors.toList());

        return DashboardStatsResponse.builder()
                .totalTickets(totalTickets)
                .openTickets(openCount)
                .inProgressTickets(inProgressCount)
                .resolvedTickets(resolvedCount)
                .closedTickets(closedCount)
                .overdueTickets(overdueCount)
                .ticketsByStatus(statusMetrics)
                .ticketsByCategory(categoryMetrics)
                .build();
    }
}
