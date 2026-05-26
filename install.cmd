@echo off
REM M.I.C. one-click installer for Windows.
REM Adds <this folder>/bin to your user PATH and writes ~/.mic/config.json.
REM Safe to run multiple times - idempotent.

python "%~dp0install.py"
echo.
pause
