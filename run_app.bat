@echo off
title AgriWatch Goa - AI Crop Stress Platform
cd /d "%~dp0"

echo =====================================================================
echo   AgriWatch Goa - AI Crop Stress & Farm Early-Warning Platform
echo =====================================================================
echo.
echo Launching Streamlit application...
echo The dashboard will open automatically in your browser at:
echo http://localhost:8501
echo.
echo (Keep this window open while using the platform)
echo Press Ctrl+C to stop the application.
echo =====================================================================
echo.

python -m streamlit run app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [Notice] Trying with 'py' launcher...
    py -m streamlit run app.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Could not start the application.
    echo If needed, run: pip install -r requirements.txt
    pause
)
