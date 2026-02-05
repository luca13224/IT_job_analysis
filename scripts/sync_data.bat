@echo off
chcp 65001 >nul
echo.
echo 🔄 Syncing data files...
echo.

REM Change to project root
cd /d "%~dp0\.."

REM Verify data in standard location
if exist "data\processed\clean_data.csv" (
    echo ✅ Data ready: data\processed\clean_data.csv
    echo.
    python -c "import pandas as pd; df=pd.read_csv('data/processed/clean_data.csv'); print(f'📊 Jobs: {len(df):,}')"
) else (
    echo ❌ Data file not found!
)

echo.
