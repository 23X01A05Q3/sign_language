@echo off
setlocal
echo ==========================================
echo    SignSpeak AI Pro - Startup Script
echo ==========================================

:: 1. Check if node_modules exists in web directory
if not exist "web\node_modules\" (
    echo [INFO] Installing web application dependencies...
    cd web && npm install && cd ..
)

:: 2. Start the Flask ML Backend
echo [INFO] Launching Python Backend (Port 5000)...
start "SignSpeak Backend" cmd /c ".\venv\Scripts\python server.py"

:: 3. Start the Vite Web Dashboard
echo [INFO] Launching Web Dashboard (Port 5173)...
start "SignSpeak Dashboard" cmd /c "cd web && npm run dev"

:: 4. Wait a few seconds for servers to initialize
echo [INFO] Waiting for initialization...
timeout /t 5 /nobreak > nul

:: 5. Open the Dashboard in the default browser
echo [INFO] Opening browser...
start http://localhost:5173

echo.
echo ------------------------------------------
echo SUCCESS: SignSpeak AI is starting up!
echo.
echo If the dashboard doesn't appear, please visit:
echo http://localhost:5173
echo ------------------------------------------
echo.
echo Press any key to stop the help script (servers will keep running in their own windows).
pause > nul
