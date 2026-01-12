@echo off

REM Activate Anaconda base environment
call C:\Users\vvyloi02\AppData\Local\anaconda3\condabin\conda activate base
echo Conda base environment activated

REM Run the connect.py script
start "" python3 "%~dp0..\resources\leica_disto_connect\connect.py"

cd ..
set PYTHONPATH=%CD%
cd src
python3 main.py