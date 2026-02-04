@echo off
REM Quick Start Script for Vietnam IT Job Market Analysis

echo ================================================
echo Vietnam IT Job Market Analysis - Quick Start
echo ================================================
echo.

:menu
echo Select an option:
echo.
echo 1. Run Data Processing (Clean raw data)
echo 2. Run Salary Analysis
echo 3. Run Skill Analysis
echo 4. Train ML Models
echo 5. Run Complete Pipeline
echo 6. Launch Dashboard
echo 7. Crawl New Data (ITViec)
echo 8. Install/Update Dependencies
echo 9. Exit
echo.

set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto data_processing
if "%choice%"=="2" goto salary_analysis
if "%choice%"=="3" goto skill_analysis
if "%choice%"=="4" goto ml_models
if "%choice%"=="5" goto full_pipeline
if "%choice%"=="6" goto dashboard
if "%choice%"=="7" goto crawler
if "%choice%"=="8" goto install
if "%choice%"=="9" goto end

echo Invalid choice. Please try again.
goto menu

:data_processing
echo.
echo Running Data Processing...
echo.
D:/IT-job-analysis-VN-main/.venv/Scripts/python.exe src/data_processing/processor.py
pause
goto menu

:salary_analysis
echo.
echo Running Salary Analysis...
echo.
D:/IT-job-analysis-VN-main/.venv/Scripts/python.exe src/analysis/salary_analytics.py
pause
goto menu

:skill_analysis
echo.
echo Running Skill Analysis...
echo.
D:/IT-job-analysis-VN-main/.venv/Scripts/python.exe src/nlp/skill_analyzer.py
pause
goto menu

:ml_models
echo.
echo Training ML Models...
echo.
D:/IT-job-analysis-VN-main/.venv/Scripts/python.exe src/ml_models/salary_prediction.py
pause
goto menu

:full_pipeline
echo.
echo Running Complete Pipeline...
echo.
D:/IT-job-analysis-VN-main/.venv/Scripts/python.exe main.py
pause
goto menu

:dashboard
echo.
echo Launching Dashboard...
echo Open your browser at: http://localhost:8501
echo.
D:/IT-job-analysis-VN-main/.venv/Scripts/streamlit.exe run src/visualization/dashboard.py
pause
goto menu

:crawler
echo.
echo Starting Web Crawler...
echo Please login to ITViec when browser opens...
echo.
D:/IT-job-analysis-VN-main/.venv/Scripts/python.exe src/crawler/ITViec_crawling.py
pause
goto menu

:install
echo.
echo Installing/Updating Dependencies...
echo.
D:/IT-job-analysis-VN-main/.venv/Scripts/python.exe -m pip install --upgrade pip
D:/IT-job-analysis-VN-main/.venv/Scripts/pip.exe install -r requirements.txt
echo.
echo Dependencies installed successfully!
pause
goto menu

:end
echo.
echo Thank you for using Vietnam IT Job Market Analysis!
echo.
exit
