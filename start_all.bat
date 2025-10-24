@echo off
echo Starting AI Quiz Application...
echo.

REM Check if OpenAI API key is configured
findstr /C:"sk-proj-placeholder" ai-service\.env >nul
if %errorlevel%==0 (
    echo ❌ IMPORTANT: OpenAI API key not configured!
    echo Please edit ai-service\.env and replace the placeholder with your actual OpenAI API key
    echo Get your key from: https://platform.openai.com/api-keys
    echo.
    pause
    exit /b 1
)

echo ✅ Starting AI Service...
start "AI Service" cmd /k "cd ai-service\src && python app.py"

timeout /t 3 /nobreak >nul

echo ✅ Starting Backend...
start "Backend" cmd /k "cd ai_backend && npm run dev"

timeout /t 3 /nobreak >nul

echo ✅ Starting Frontend...
start "Frontend" cmd /k "cd ai_frontend && npm start"

echo.
echo ✅ All services started!
echo Frontend: http://localhost:3000
echo Backend: http://localhost:5000
echo AI Service: http://localhost:8000
echo.
echo Press any key to close this window...
pause >nul