@echo off
echo ========================================
echo  Running Enhanced Dashboard
echo ========================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting enhanced dashboard...
echo Dashboard will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run src\visualization\dashboard_v2.py

pause
