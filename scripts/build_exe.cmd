@echo off
setlocal
cd /d "%~dp0\.."

set "PYTHON=.venv\Scripts\python.exe"
for %%I in ("data\documents\manual_v2026_3") do set "MANUAL_SOURCE=%%~fI"
if not exist "%PYTHON%" (
    echo Ambiente Python ausente. Crie .venv e instale os extras de desenvolvimento.
    exit /b 1
)
if not exist "data\documents\manual_v2026_3\manifesto.json" (
    echo Base modular v2026.3 ausente.
    exit /b 1
)
if not exist "build" mkdir build

"%PYTHON%" -m PyInstaller --clean --noconfirm --onefile --console --name ExtratorOcorrencias --paths src --specpath build --add-data "%MANUAL_SOURCE%;data\documents\manual_v2026_3" packaging\entrypoint.py
if errorlevel 1 exit /b 1

echo Executavel criado em dist\ExtratorOcorrencias.exe
