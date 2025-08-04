@echo off
echo ================================================
echo VeriSure Flask Application
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "flask_app.py" (
    echo Error: flask_app.py not found
    echo Please run this script from the application directory
    pause
    exit /b 1
)

REM Install Flask dependencies if needed
echo Checking Flask dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing Flask dependencies...
    pip install -r requirements_flask.txt
    if errorlevel 1 (
        echo Error: Failed to install Flask dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting Flask application...
echo Flask app will be available at: http://localhost:5000
echo Streamlit app can still be run separately at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the Flask application
echo ================================================
echo.

REM Run the Flask application
python run_flask.py

pause 