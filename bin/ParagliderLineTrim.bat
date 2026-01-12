@echo off

REM Initialize Conda for cmd.exe
call "%USERPROFILE%\AppData\Local\anaconda3\Scripts\activate.bat"

REM Activate Anaconda base environment
call conda activate base
echo Conda base environment activated

REM Run the connect.py script from hardware/leica_disto/ in a separate window
start "Leica Disto Connect" cmd /k "conda activate base && python "%~dp0..\hardware\leica_disto\connect.py""

REM Change to project root and set PYTHONPATH
cd /d "%~dp0.."
set PYTHONPATH=%CD%

REM Run the main application
cd src
python main.py