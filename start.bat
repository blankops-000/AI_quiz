@echo off
echo Starting AI Quiz Application...
echo.

echo Installing dependencies...
call npm install
if %errorlevel% neq 0 (
    echo Failed to install root dependencies
    pause
    exit /b 1
)

echo Installing backend dependencies...
cd ai_backend
call npm install
if %errorlevel% neq 0 (
    echo Failed to install backend dependencies
    pause
    exit /b 1
)
cd ..

echo Installing frontend dependencies...
cd ai_frontend
call npm install
if %errorlevel% neq 0 (
    echo Failed to install frontend dependencies
    pause
    exit /b 1
)
cd ..

echo Installing AI service dependencies...
cd ai-service
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install AI service dependencies
    echo Make sure Python is installed and accessible
    pause
    exit /b 1
)
cd ..

echo.
echo All dependencies installed successfully!
echo.
echo Starting all services...
echo - Backend will run on http://localhost:5000
echo - Frontend will run on http://localhost:3000  
echo - AI Service will run on http://localhost:8000
echo.

start "AI Service" cmd /k "cd ai-service\src && python app.py"
timeout /t 3 /nobreak > nul

start "Backend" cmd /k "cd ai_backend && npm run dev"
timeout /t 3 /nobreak > nul

start "Frontend" cmd /k "cd ai_frontend && npm start"

echo.
echo All services are starting...
echo Check the opened terminal windows for status
echo.
pause