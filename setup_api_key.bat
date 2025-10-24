@echo off
echo OpenAI API Key Setup
echo ====================
echo.
echo 1. Go to: https://platform.openai.com/api-keys
echo 2. Create a new API key
echo 3. Copy the key (starts with sk-)
echo 4. Enter it below:
echo.
set /p apikey="Enter your OpenAI API key: "

if "%apikey%"=="" (
    echo No API key entered. Exiting...
    pause
    exit /b 1
)

REM Update the .env file
powershell -Command "(Get-Content 'ai-service\.env') -replace 'OPENAI_API_KEY=sk-proj-placeholder.*', 'OPENAI_API_KEY=%apikey%' | Set-Content 'ai-service\.env'"

echo.
echo ✅ API key configured successfully!
echo You can now run start_all.bat to start the application
echo.
pause