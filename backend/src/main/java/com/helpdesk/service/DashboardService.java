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

import java.time.Duration;
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

        // Tinh toan MTTA va MTTR thuc te
        long totalMttaMinutes = 0;
        long mttaCount = 0;

        long totalMttrMinutes = 0;
        long mttrCount = 0;

        Map<String, Long> categoryCountMap = new HashMap<>();
        List<Category> allCategories = categoryRepository.findAll();
        for (Category cat : allCategories) {
            categoryCountMap.put(cat.getName(), 0L);
        }

        Map<String, Long> departmentCountMap = new HashMap<>();

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

            // Đo lường MTTA (thời gian tiếp nhận từ lúc tạo)
            if (ticket.getCreatedAt() != null && ticket.getAcknowledgedAt() != null) {
                long minutes = Duration.between(ticket.getCreatedAt(), ticket.getAcknowledgedAt()).toMinutes();
                if (minutes >= 0) {
                    totalMttaMinutes += minutes;
                    mttaCount++;
                }
            }

            // Đo lường MTTR (thời gian giải quyết từ lúc tạo)
            if (ticket.getCreatedAt() != null && ticket.getResolvedAt() != null) {
                long minutes = Duration.between(ticket.getCreatedAt(), ticket.getResolvedAt()).toMinutes();
                if (minutes >= 0) {
                    totalMttrMinutes += minutes;
                    mttrCount++;
                }
            }

            // Đếm theo danh mục
            if (ticket.getCategory() != null) {
                String catName = ticket.getCategory().getName();
                categoryCountMap.put(catName, categoryCountMap.getOrDefault(catName, 0L) + 1);
            }

            // Đếm theo phòng ban
            String deptName = (ticket.getRequester() != null && ticket.getRequester().getDepartment() != null && !ticket.getRequester().getDepartment().isBlank())
                    ? ticket.getRequester().getDepartment()
                    : "Khác";
            departmentCountMap.put(deptName, departmentCountMap.getOrDefault(deptName, 0L) + 1);
        }

        // Định dạng MTTA
        Double mttaMinutes = mttaCount > 0 ? (double) totalMttaMinutes / mttaCount : 0.0;
        String mttaFormatted;
        if (mttaCount == 0) {
            mttaFormatted = "Chưa có dữ liệu";
        } else if (mttaMinutes < 60) {
            mttaFormatted = Math.round(mttaMinutes) + " phút";
        } else {
            mttaFormatted = String.format(Locale.US, "%.1f giờ", mttaMinutes / 60.0);
        }

        // Định dạng MTTR
        Double mttrHours = mttrCount > 0 ? ((double) totalMttrMinutes / mttrCount) / 60.0 : 0.0;
        String mttrFormatted;
        if (mttrCount == 0) {
            mttrFormatted = "Chưa có dữ liệu";
        } else if (mttrHours < 1.0) {
            mttrFormatted = Math.round(mttrHours * 60) + " phút";
        } else {
            mttrFormatted = String.format(Locale.US, "%.1f giờ", mttrHours);
        }

        // Tỷ lệ SLA
        long slaMetCount = totalTickets > 0 ? Math.max(0, totalTickets - overdueCount) : 0;
        double slaCompliance = totalTickets > 0 ? Math.round((slaMetCount * 100.0 / totalTickets) * 10.0) / 10.0 : 100.0;

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

        List<DashboardStatsResponse.DepartmentMetric> departmentMetrics = departmentCountMap.entrySet().stream()
                .map(entry -> DashboardStatsResponse.DepartmentMetric.builder()
                        .departmentName(entry.getKey())
                        .count(entry.getValue())
                        .build())
                .sorted(Comparator.comparing(DashboardStatsResponse.DepartmentMetric::getCount).reversed())
                .collect(Collectors.toList());

        return DashboardStatsResponse.builder()
                .totalTickets(totalTickets)
                .openTickets(openCount)
                .inProgressTickets(inProgressCount)
                .resolvedTickets(resolvedCount)
                .closedTickets(closedCount)
                .overdueTickets(overdueCount)
                .slaComplianceRate(slaCompliance)
                .slaMetTickets(slaMetCount)
                .mttaMinutes(mttaMinutes)
                .mttaFormatted(mttaFormatted)
                .mttaCount(mttaCount)
                .mttrHours(mttrHours)
                .mttrFormatted(mttrFormatted)
                .mttrCount(mttrCount)
                .ticketsByStatus(statusMetrics)
                .ticketsByCategory(categoryMetrics)
                .ticketsByDepartment(departmentMetrics)
                .build();
    }
}
