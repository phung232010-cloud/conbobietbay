@echo off
chcp 65001 >nul
title Deploy Gen AI Exam Hub to Vercel
echo ====================================================================
echo   HỆ THỐNG TRIỂN KHAI TỰ ĐỘNG LÊN VERCEL (GEN AI FOUNDATIONS HUB)
echo ====================================================================
echo.
echo [1/2] Đang xác thực tài khoản Vercel...
echo (Trình duyệt sẽ tự động mở để bạn đăng nhập Vercel qua GitHub/Google/Email)
echo.
call npx.cmd --yes vercel login
echo.
echo [2/2] Đang đẩy toàn bộ trang web lên Vercel Production (*.vercel.app)...
call npx.cmd --yes vercel --prod --yes
echo.
echo ====================================================================
echo   TRIỂN KHAI HOÀN TẤT! TRANG WED ĐÃ SẴN SÀNG TRÊN VERCEL.APP
echo ====================================================================
pause
