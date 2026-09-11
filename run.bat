@echo off
title Multimodal Infant Distress Monitor (Slim 320 + BabyCry AI)
cd /d "%~dp0"

echo ================================================================
echo   MULTIMODAL INFANT DISTRESS MONITOR
echo   Face Emotion AI (Slim 320) + BabyCry AI Acoustics
echo ================================================================
echo.

if not exist "venv\Scripts\python.exe" (
    echo Virtual environment not detected! Creating one now...
    py -3.10 -m venv venv || "C:\ProgramData\anaconda3\python.exe" -m venv venv
    call .\venv\Scripts\pip.exe install -r requirements.txt
)

if not exist "models\version-slim-320.onnx" (
    echo Downloading pre-trained face detection and emotion models...
    call .\venv\Scripts\python.exe download_models.py
)

:MENU
echo.
echo Please select an operating mode:
echo   [1] Launch Multimodal Web Dashboard (Browser http://localhost:5000)
echo   [2] Live Webcam Real-Time Window (OpenCV HUD)
echo   [3] Analyze Sample Face Image
echo   [4] Run Face Emotion Verification Test
echo   [5] Run Multimodal Baby Cry Verification Test
echo   [6] Exit
echo.
set /p choice="Enter option [1-6]: "

if "%choice%"=="1" (
    echo Starting Multimodal Web Dashboard on http://localhost:5000...
    start http://localhost:5000
    .\venv\Scripts\python.exe web_app.py
    goto MENU
)
if "%choice%"=="2" (
    echo Starting Webcam inference...
    .\venv\Scripts\python.exe main.py --mode webcam
    goto MENU
)
if "%choice%"=="3" (
    echo Analyzing sample.jpg...
    .\venv\Scripts\python.exe main.py --mode image --input sample.jpg
    start annotated_sample.jpg
    goto MENU
)
if "%choice%"=="4" (
    echo Running face pipeline tests...
    .\venv\Scripts\python.exe test_pipeline.py
    goto MENU
)
if "%choice%"=="5" (
    echo Running multimodal integration tests...
    .\venv\Scripts\python.exe test_multimodal.py
    goto MENU
)
if "%choice%"=="6" (
    echo Exiting...
    exit /b
)

echo Invalid choice, please try again.
goto MENU
