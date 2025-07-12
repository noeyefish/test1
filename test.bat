@echo off
set /p answer=האם להמשיך? (כן/לא): 

if /i "%answer%"=="כן" (
    echo שלום
    pause
) else (
    echo הופסק.
    pause
)
