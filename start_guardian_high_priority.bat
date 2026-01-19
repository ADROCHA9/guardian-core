@echo off
echo [Guardian] Iniciando Guardian en modo headless...

REM === Ir al directorio del proyecto ===
cd /d C:\Users\CONECTIA BA\guardian_bot

REM === Iniciar Guardian sin consola ===
start "" pythonw run_guardian_headless.py

REM === Esperar a que el proceso arranque ===
timeout /t 2 /nobreak > nul

echo [Guardian] Ajustando prioridad del proceso...

REM === Subir prioridad a ALTA usando PowerShell ===
powershell -Command ^
  "Get-Process pythonw -ErrorAction SilentlyContinue | Where-Object { $_.Path -like '*guardian_bot*' } | ForEach-Object { $_.PriorityClass = 'High' }"

echo [Guardian] Guardian ejecutándose con prioridad ALTA.
echo [Guardian] Script finalizado. Guardian seguirá en segundo plano.