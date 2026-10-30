package com.helpdesk.service;

import com.helpdesk.entity.User;
import com.helpdesk.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserService {

    private final UserRepository userRepository;

    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id);
    }

    public Optional<User> getUserByUsername(String username) {
        return userRepository.findByUsername(username);
    }

    @Transactional
    public User createUser(User user) {
        if (user.getUsername() == null || user.getUsername().trim().isEmpty()) {
            throw new IllegalArgumentException("Tên đăng nhập không được để trống!");
        }
        if (userRepository.findByUsername(user.getUsername().trim()).isPresent()) {
            throw new IllegalArgumentException("Tên đăng nhập '" + user.getUsername().trim() + "' đã tồn tại!");
        }
        if (user.getEmail() != null && !user.getEmail().trim().isEmpty()) {
            if (userRepository.findByEmail(user.getEmail().trim()).isPresent()) {
                throw new IllegalArgumentException("Email '" + user.getEmail().trim() + "' đã tồn tại!");
            }
        }
        if (user.getPassword() == null || user.getPassword().isBlank()) {
            user.setPassword("123456"); // Mật khẩu mặc định
        }
        if (user.getFullName() == null || user.getFullName().trim().isEmpty()) {
            user.setFullName(user.getUsername());
        }
        return userRepository.save(user);
    }

    @Transactional
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
}
