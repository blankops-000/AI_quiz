@echo off
echo Starting AI Quiz Application (Backend + Frontend only)...
echo.

echo Starting Backend...
start "Backend" cmd /k "cd ai_backend && npm run dev"
timeout /t 3 /nobreak > nul

echo Starting Frontend...
start "Frontend" cmd /k "cd ai_frontend && npm start"

echo.
echo Services starting...
echo - Backend: http://localhost:5000
echo - Frontend: http://localhost:3000
echo.
echo Note: AI features will use mock data from backend
pause