@echo off
cd /d %~dp0
start "backend" cmd /k "call backend\.venv\Scripts\activate.bat && cd backend && python app.py"
cd frontend
call npm run dev
