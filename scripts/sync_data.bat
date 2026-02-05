@echo off
chcp 65001 >nul
echo.
echo 🔄 Syncing data files...
echo.

REM Change to project root
cd /d "%~dp0\.."

REM Copy from new location to old location
copy /Y "data\processed\clean_data.csv" "data_clean\clean_data.csv" >nul

if %errorlevel% equ 0 (
    echo ✅ Synced: data\processed → data_clean
    echo.
    python -c "import pandas as pd; df=pd.read_csv('data_clean/clean_data.csv'); print(f'📊 Jobs: {len(df):,}')"
) else (
    echo ❌ Sync failed!
)

echo.
