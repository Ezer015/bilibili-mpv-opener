@echo off
REM Windows batch script to open Bilibili video in MPV
REM Usage: open_in_mpv.bat [bilibili_url]

:: Run with Python 3
call python "%~dp0open_in_mpv.py" %1

exit /b 0
