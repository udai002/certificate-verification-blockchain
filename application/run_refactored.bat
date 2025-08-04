@echo off
echo Starting Refactored VeriSure Flask Application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "flask_app_refactored.py" (
    echo Error: flask_app_refactored.py not found
    echo Please make sure you're in the correct directory
    pause
    exit /b 1
)

if not exist "templates" (
    echo Error: templates directory not found
    echo Please make sure all template files are present
    pause
    exit /b 1
)

if not exist "static" (
    echo Error: static directory not found
    echo Please make sure all static files are present
    pause
    exit /b 1
)

echo Checking dependencies...
pip install -r requirements_flask.txt >nul 2>&1

echo.
echo Starting Flask application...
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the application
echo.

python flask_app_refactored.py

pause 