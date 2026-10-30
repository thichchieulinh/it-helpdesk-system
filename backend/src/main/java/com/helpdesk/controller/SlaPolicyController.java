package com.helpdesk.controller;

import com.helpdesk.entity.SlaPolicy;
import com.helpdesk.repository.SlaPolicyRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/sla-policies")
@RequiredArgsConstructor
public class SlaPolicyController {

    private final SlaPolicyRepository slaPolicyRepository;

    @GetMapping
    public ResponseEntity<List<SlaPolicy>> getAllPolicies() {
        return ResponseEntity.ok(slaPolicyRepository.findAll());
    }

    @PutMapping("/{id}")
    public ResponseEntity<SlaPolicy> updatePolicy(
            @PathVariable Long id,
            @RequestBody SlaPolicy req
    ) {
        return slaPolicyRepository.findById(id)
                .map(policy -> {
                    if (req.getResolutionTimeHours() != null) {
                        policy.setResolutionTimeHours(req.getResolutionTimeHours());
                    }
                    return ResponseEntity.ok(slaPolicyRepository.save(policy));
                })
                .orElse(ResponseEntity.notFound().build());
    }
}
