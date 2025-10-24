@echo off
echo Starting AI Quiz Application with ChatGPT Integration...
echo.
echo IMPORTANT: Make sure to set your OpenAI API key in ai-service\.env
echo.

echo Starting Backend...
start "Backend" cmd /k "cd ai_backend && npm run dev"
timeout /t 3 /nobreak > nul

echo Starting ChatGPT AI Service...
start "AI Service" cmd /k "cd ai-service\src && python app-chatgpt.py"
timeout /t 3 /nobreak > nul

echo Starting Frontend...
start "Frontend" cmd /k "cd ai_frontend && npm start"

echo.
echo All services starting...
echo - Backend: http://localhost:5000
echo - AI Service (ChatGPT): http://localhost:8000
echo - Frontend: http://localhost:3000
echo.
echo Note: AI features now use ChatGPT for better responses!
pause