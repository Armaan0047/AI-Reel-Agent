@echo off
:: ═══════════════════════════════════════════════════════════════
::  AI REEL AGENT v5.0 — Launcher
::  Developed by Master Armaan
:: ═══════════════════════════════════════════════════════════════

title AI Reel Agent v5.0 — by Master Armaan
color 0A
mode con: cols=120 lines=40

:: Navigate to script directory
cd /d "%~dp0"

echo.
echo    ╔════════════════════════════════════════════╗
echo    ║     AI REEL AGENT v5.0 — LAUNCHER         ║
echo    ║     Developed by Master Armaan             ║
echo    ╚════════════════════════════════════════════╝
echo.

:: ─── Check Python ────────────────────────────────────────────
echo    [*] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo    [ERROR] Python not found!
    echo    Please install Python 3.10+ from https://python.org
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%V in ('python --version 2^>^&1') do (
    echo    [OK] Python %%V detected
)

:: ─── Check FFmpeg (via imageio-ffmpeg) ───────────────────────
echo    [*] Checking FFmpeg...
python -c "from imageio_ffmpeg import get_ffmpeg_exe; print(get_ffmpeg_exe())" >nul 2>&1
if errorlevel 1 (
    echo    [WARN] FFmpeg not bundled yet. Will install with dependencies.
) else (
    echo    [OK] FFmpeg ready (imageio-ffmpeg)
)

:: ─── Auto-install dependencies ───────────────────────────────
echo    [*] Checking dependencies...
pip install -r requirements.txt --quiet 2>nul
if errorlevel 1 (
    echo    [WARN] Some dependencies may have failed to install.
) else (
    echo    [OK] All dependencies installed
)

echo.
echo    ────────────────────────────────────────────
echo    [*] Launching AI Reel Agent...
echo    ────────────────────────────────────────────
echo.

:: ─── Launch Application ──────────────────────────────────────
python main.py %*

echo.
echo    ────────────────────────────────────────────
echo    [*] AI Reel Agent session ended.
echo    ────────────────────────────────────────────
pause
