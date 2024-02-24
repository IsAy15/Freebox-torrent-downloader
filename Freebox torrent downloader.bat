@echo off
setlocal enableExtensions disableDelayedExpansion
python main.py %*
PAUSE
endlocal
goto :eof
