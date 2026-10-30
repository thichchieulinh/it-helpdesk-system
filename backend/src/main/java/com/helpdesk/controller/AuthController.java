package com.helpdesk.controller;

import com.helpdesk.dto.LoginRequest;
import com.helpdesk.entity.User;
import com.helpdesk.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final UserRepository userRepository;

    /**
     * Xác thực đăng nhập đơn giản cho hệ thống nội bộ / demo switch role
     */
    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest req) {
        if (req.getUsername() == null || req.getUsername().trim().isEmpty()) {
            return ResponseEntity.badRequest().body("Tên đăng nhập không được để trống");
        }

        Optional<User> userOpt = userRepository.findByUsername(req.getUsername().trim());
        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Tài khoản không tồn tại trên hệ thống");
        }

        User user = userOpt.get();

        // Kiểm tra mật khẩu (hỗ trợ kiểm tra mật khẩu thật hoặc chế độ demo)
        if (req.getPassword() != null && !req.getPassword().isEmpty()) {
            if (!req.getPassword().equals(user.getPassword())) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Mật khẩu không chính xác");
            }
        }

        return ResponseEntity.ok(user);
    }

    /**
     * Danh sách tài khoản demo cho giao diện Login 1-click
     */
    @GetMapping("/users")
    public ResponseEntity<List<User>> getDemoUsers() {
        return ResponseEntity.ok(userRepository.findAll());
    }
}
