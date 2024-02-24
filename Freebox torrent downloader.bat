@echo off
setlocal enableExtensions disableDelayedExpansion
cd /d "%~dp0"
python main.py %*
PAUSE
endlocal
goto :eof
