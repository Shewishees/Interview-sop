@echo off
chcp 65001 >nul
title Push InterviewSOP Master to GitHub
cd /d "%~dp0"
echo ========================================================
echo   ?? ???? InterviewSOP Master ? GitHub...
echo   ?? ????: https://github.com/Shewishees/Interview-sop.git
echo ========================================================
echo.
set "PATH=C:\Users\24974\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd;C:\Users\24974\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\mingw64\bin;%PATH%"
git push -u origin main
echo.
if %ERRORLEVEL% equ 0 (
    echo ========================================================
    echo   ?? ??????????? GitHub?
    echo ========================================================
) else (
    echo ========================================================
    echo   ?? ????????? GitHub ????????
    echo ========================================================
)
echo.
pause
