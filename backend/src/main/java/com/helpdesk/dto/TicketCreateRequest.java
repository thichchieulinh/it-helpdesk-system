package com.helpdesk.dto;

import com.helpdesk.entity.enums.Priority;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TicketCreateRequest {
    private String title;
    private String description;
    private Priority priority;
    private Long categoryId;
    private Long requesterId;
}
