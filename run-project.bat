@echo off
chcp 65001 >nul
title Khởi động Hệ thống IT Helpdesk Ticketing System

echo ======================================================================
echo    KHỞI ĐỘNG HỆ THỐNG IT HELPDESK TICKETING SYSTEM
echo    - Backend: Spring Boot 3 (Port 8080)
echo    - Frontend: ReactJS + Tailwind CSS (Port 5173)
echo ======================================================================
echo.

echo [1/3] Đang khởi động Backend (Spring Boot)...
start "Backend - Spring Boot (Port 8080)" cmd /k "cd /d "%~dp0backend" && mvnw.cmd spring-boot:run"

echo [2/3] Đang khởi động Frontend (ReactJS Vite)...
start "Frontend - ReactJS (Port 5173)" cmd /k "cd /d "%~dp0frontend" && npm.cmd run dev"

echo.
echo [3/3] Đang chờ 5 giây để máy chủ khởi động rồi mở trình duyệt...
timeout /t 5 >nul
start http://localhost:5173

echo.
echo ======================================================================
echo  Hệ thống đã được bật trong 2 cửa sổ riêng biệt!
echo  - Giao diện ứng dụng: http://localhost:5173
echo  - H2 Database Console: http://localhost:8080/h2-console
echo  (Để tắt hệ thống: Đóng 2 cửa sổ đen đang chạy hoặc bấm Ctrl + C)
echo ======================================================================
pause
