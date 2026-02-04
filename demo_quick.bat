@echo off
chcp 65001 >nul
echo ========================================
echo   ⚡ DEMO NHANH - CHỈ DASHBOARD
echo ========================================
echo.

cd /d "%~dp0"

echo Kích hoạt môi trường...
call .venv\Scripts\activate.bat

echo.
echo 🌐 Khởi động Dashboard...
echo Mở trình duyệt: http://localhost:8501
echo Nhấn Ctrl+C để dừng
echo.

streamlit run src\visualization\dashboard_v2.py

pause
