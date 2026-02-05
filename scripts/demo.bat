@echo off
chcp 65001 >nul
color 0B
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🎬 DEMO CHUYÊN NGHIỆP: CRAWL → PROCESS → DASHBOARD         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📋 Quy trình sẽ tự động:
echo    1️⃣  Browser mở → Crawl ITViec (5 jobs)
echo    2️⃣  Xử lý data (Clean + Transform + Merge)
echo    3️⃣  Dashboard tự động mở (10 pages)
echo.
echo ⏱️  Thời gian: ~2 phút
echo.
pause

cls
echo.
echo ══════════════════════════════════════════════════════════════
echo  BƯỚC 1/3: CRAWL DATA TỪ ITVIEC
echo ══════════════════════════════════════════════════════════════
echo.
echo 🌐 Browser đang khởi động...
echo 🤖 AI Groq sẽ phân tích HTML và extract data
echo.

REM Chạy crawler - browser sẽ hiện lên
python src/crawler/ITViec_AI_groq.py --jobs 5

if %errorlevel% neq 0 (
    echo.
    echo ❌ Lỗi crawl! Kiểm tra:
    echo    - GROQ_API_KEY trong .env
    echo    - Internet connection
    echo    - playwright install chromium
    pause
    exit /b 1
)

echo.
echo ✅ Crawl hoàn tất!

REM Data already in standard location: data/processed/clean_data.csv
echo ✅ Data location: data/processed/clean_data.csv

timeout /t 2 >nul

cls
echo.
echo ══════════════════════════════════════════════════════════════
echo  BƯỚC 2/3: XỬ LÝ DATA
echo ══════════════════════════════════════════════════════════════
echo.
echo ⚙️  Đang xử lý...
echo    ✓ Clean duplicates
echo    ✓ Transform columns
echo    ✓ Extract salary
echo    ✓ Merge to clean_data.csv
echo.

REM Hiển thị stats nhanh
python -c "import pandas as pd; df=pd.read_csv('data/processed/clean_data.csv'); print(f'📊 Total: {len(df)} jobs | 🏢 {df[\"company_names\"].nunique()} companies')"

echo.
echo ✅ Xử lý hoàn tất!
timeout /t 2 >nul

cls
echo.
echo ══════════════════════════════════════════════════════════════
echo  BƯỚC 3/3: KHỞI ĐỘNG DASHBOARD
echo ══════════════════════════════════════════════════════════════
echo.
echo 🚀 Đang start Streamlit...
echo 🌐 Dashboard sẽ tự động mở trong browser
echo.
echo 📊 10 pages:
echo    • Overview  • Skills  • Salary  • Companies
echo    • ML Recommendation  • Career Simulator  • ...
echo.

REM Start dashboard in background
start /B streamlit run src/visualization/dashboard_v2.py

REM Đợi dashboard ready
echo ⏳ Chờ dashboard khởi động...
timeout /t 4 >nul

REM Mở browser
start http://localhost:8501

cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  ✅ DEMO HOÀN TẤT                                            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📊 KẾT QUẢ:

python -c "import pandas as pd; df=pd.read_csv('data/processed/clean_data.csv'); print(f'   📈 {len(df)} jobs từ {df[\"company_names\"].nunique()} companies'); print(f'   🌐 Dashboard: http://localhost:8501')"

echo.
echo 🎯 QUY TRÌNH:
echo    Web → AI Crawl → Raw CSV → Clean → Transform → Dashboard
echo.
echo 💡 Lưu ý:
echo    • Dashboard đang chạy ở background
echo    • Ctrl+C trong terminal để stop
echo    • Refresh browser để thấy data mới
echo.
echo ══════════════════════════════════════════════════════════════
echo.

pause
