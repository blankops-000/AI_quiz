@echo off
echo Starting AI Service...
cd ai-service\src

REM Try different Python paths
if exist "C:\Python312\python.exe" (
    "C:\Python312\python.exe" app.py
) else if exist "C:\Python311\python.exe" (
    "C:\Python311\python.exe" app.py
) else if exist "C:\Python310\python.exe" (
    "C:\Python310\python.exe" app.py
) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" app.py
) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" app.py
) else if exist "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe" (
    "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe" app.py
) else (
    echo Python not found. Please install Python or add it to PATH.
    echo You can download Python from: https://python.org/downloads
    pause
)