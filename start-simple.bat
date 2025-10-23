@echo off
echo Starting AI Quiz Application (Simplified)...
echo.

echo Starting Backend...
start "Backend" cmd /k "cd ai_backend && npm start"
timeout /t 3 /nobreak > nul

echo Starting AI Service...
start "AI Service" cmd /k "cd ai-service\src && python app-simple.py"
timeout /t 3 /nobreak > nul

echo Starting Frontend...
start "Frontend" cmd /k "cd ai_frontend && npm start"

echo.
echo All services are starting...
echo - Backend: http://localhost:5000
echo - AI Service: http://localhost:8000
echo - Frontend: http://localhost:3000
echo.
pause