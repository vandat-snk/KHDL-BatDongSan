@echo off
setlocal
set "KHDL_HTML=%~dp0outputs\DASHBOARD_BAT_DONG_SAN.html"

if not exist "%KHDL_HTML%" (
    echo Khong tim thay dashboard. Hay chay tools\build_dashboard.py truoc.
    pause
    exit /b 1
)

rem Open an actual browser instead of the Windows .html file association.
if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" "%KHDL_HTML%"
    exit /b 0
)
if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" "%KHDL_HTML%"
    exit /b 0
)
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" "%KHDL_HTML%"
    exit /b 0
)
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    start "" "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" "%KHDL_HTML%"
    exit /b 0
)
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    start "" "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" "%KHDL_HTML%"
    exit /b 0
)

echo Khong tim thay Edge hoac Chrome tai cac thu muc thong dung.
echo Mo trinh duyet, nhan Ctrl+O va chon file:
echo "%KHDL_HTML%"
pause
exit /b 1
