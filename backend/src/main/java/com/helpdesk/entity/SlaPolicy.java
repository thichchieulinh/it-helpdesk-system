package com.helpdesk.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.helpdesk.entity.enums.Priority;
import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "sla_policies")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
public class SlaPolicy {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, unique = true, length = 20)
    private Priority priorityLevel;

    @Column(nullable = false)
    private Integer resolutionTimeHours;
}
