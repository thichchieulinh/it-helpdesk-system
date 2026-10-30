package com.helpdesk.repository;

import com.helpdesk.entity.SlaPolicy;
import com.helpdesk.entity.enums.Priority;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface SlaPolicyRepository extends JpaRepository<SlaPolicy, Long> {
    Optional<SlaPolicy> findByPriorityLevel(Priority priorityLevel);
}
