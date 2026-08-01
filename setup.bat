@echo off
REM Jarvis Phase 1 - Automatic Setup Script (Windows)
REM Run: setup.bat

setlocal enabledelayedexpansion

echo.
echo 🧠 Jarvis Phase 1 - Setup Script (Windows)
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.10+
    echo    Download from: https://www.python.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ %PYTHON_VERSION% found

REM Check Node
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Node.js not found. Frontend setup will be skipped.
    echo    Install from: https://nodejs.org
    set SKIP_FRONTEND=1
) else (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
    echo ✓ Node !NODE_VERSION! found
)

echo.
echo 📁 Setting up project structure...
echo.

REM Backend setup
echo 🔧 Setting up Backend...
cd backend

if not exist ".env" (
    echo   Creating .env file...
    copy .env.example .env >nul
    echo   ⚠️  IMPORTANT: Edit backend\.env and add your API keys:
    echo      MEM0_API_KEY=your_key_here
    echo      ANTHROPIC_API_KEY=your_key_here
) else (
    echo   ✓ .env already exists
)

if not exist "venv" (
    echo   Creating virtual environment...
    python -m venv venv
    echo   ✓ venv created
) else (
    echo   ✓ venv already exists
)

echo   Activating venv...
call venv\Scripts\activate.bat

echo   Installing dependencies...
pip install -q -r ..\requirements.txt
echo   ✓ Dependencies installed

cd ..

REM Frontend setup
if "%SKIP_FRONTEND%"=="" (
    echo.
    echo 🎨 Setting up Frontend...
    cd frontend
    
    if not exist "node_modules" (
        echo   Installing npm packages...
        call npm install -q
        echo   ✓ npm packages installed
    ) else (
        echo   ✓ node_modules already exists
    )
    
    cd ..
)

echo.
echo ==========================================
echo ✅ Setup Complete!
echo ==========================================
echo.
echo 📝 Next steps:
echo.
echo 1. Edit your API keys:
echo    Open backend\.env in your text editor
echo.
echo 2. Start backend:
echo    cd backend
echo    venv\Scripts\activate.bat
echo    python main.py
echo.

if "%SKIP_FRONTEND%"=="" (
    echo 3. Start frontend (in another terminal):
    echo    cd frontend
    echo    npm run dev
    echo.
    echo 4. Open browser:
    echo    http://localhost:3000
) else (
    echo 3. Install Node.js from https://nodejs.org
    echo.
    echo 4. Then start frontend:
    echo    cd frontend
    echo    npm install
    echo    npm run dev
)

echo.
echo 🚀 Happy hacking!
echo.
pause
