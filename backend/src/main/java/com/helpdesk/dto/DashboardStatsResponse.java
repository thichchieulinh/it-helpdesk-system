package com.helpdesk.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class DashboardStatsResponse {

    private long totalTickets;
    private long openTickets;
    private long inProgressTickets;
    private long resolvedTickets;
    private long closedTickets;
    private long overdueTickets;

    // Chi so SLA, MTTA, MTTR tinh toan thuc te
    private Double slaComplianceRate;
    private Long slaMetTickets;

    private Double mttaMinutes;
    private String mttaFormatted;
    private Long mttaCount;

    private Double mttrHours;
    private String mttrFormatted;
    private Long mttrCount;

    private List<StatusMetric> ticketsByStatus;
    private List<CategoryMetric> ticketsByCategory;
    private List<DepartmentMetric> ticketsByDepartment;

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class StatusMetric {
        private String status;
        private String label;
        private long count;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class CategoryMetric {
        private String categoryName;
        private long count;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class DepartmentMetric {
        private String departmentName;
        private long count;
    }
}
