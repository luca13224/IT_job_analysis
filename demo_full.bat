@echo off
chcp 65001 >nul
echo ========================================
echo   🤖 DEMO AI JOB ANALYSIS - FULL FLOW
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Kích hoạt môi trường Python...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Lỗi: Không tìm thấy virtual environment
    echo Vui lòng chạy: python -m venv .venv
    pause
    exit /b 1
)

echo ✅ Môi trường đã kích hoạt
echo.

echo [2/4] Chạy AI Crawler Demo...
echo --------------------------------------------------
python src/crawler/ITViec_AI_demo.py
if errorlevel 1 (
    echo ⚠️ Cảnh báo: AI Crawler gặp lỗi nhưng tiếp tục...
)
echo.

echo [3/4] Kiểm tra dữ liệu...
if exist "data_clean\clean_data.csv" (
    echo ✅ Dữ liệu có sẵn: data_clean\clean_data.csv
) else (
    echo ⚠️ Không tìm thấy data_clean\clean_data.csv
    echo Sử dụng data_raw\ITViec_data.csv thay thế...
)
echo.

echo [4/4] Khởi động Dashboard...
echo --------------------------------------------------
echo 🌐 Dashboard sẽ mở tại: http://localhost:8501
echo 📚 Xem hướng dẫn chi tiết: QUICK_START.md
echo.
echo 💡 Nhấn Ctrl+C để dừng dashboard
echo ========================================
echo.

streamlit run src\visualization\dashboard_v2.py

pause
