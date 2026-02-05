@echo off
chcp 65001 >nul
cls
echo.
echo 🚀 Starting Dashboard...
echo.

REM Change to project root (parent of scripts)
cd /d "%~dp0\.."

REM Check if file exists
if not exist "src\visualization\dashboard_v2.py" (
    echo ❌ Error: dashboard_v2.py not found
    echo 📁 Current dir: %CD%
    pause
    exit /b 1
)

echo 🌐 Opening: http://localhost:8501
echo.

streamlit run src\visualization\dashboard_v2.py
