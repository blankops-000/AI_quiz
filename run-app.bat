@echo off
echo Killing existing processes...
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak > nul

echo Starting AI Quiz Application...
echo.

echo Starting Backend on port 5000...
start "Backend" cmd /k "cd ai_backend && npm run dev"
timeout /t 5 /nobreak > nul

echo Starting Frontend on port 3000...
start "Frontend" cmd /k "cd ai_frontend && npm start"

echo.
echo Application is starting...
echo - Backend: http://localhost:5000
echo - Frontend: http://localhost:3000
echo.
echo Note: AI service requires Python installation
echo For full AI features, install Python and run start-with-chatgpt.bat
echo.
pause