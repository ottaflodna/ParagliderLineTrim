@echo off

REM Activate Anaconda base environment
call C:\Users\vvyloi02\AppData\Local\anaconda3\condabin\conda activate base
echo Conda base environment activated

REM Run the connect.py script from hardware/leica_disto/
start "" python3 "%~dp0..\hardware\leica_disto\connect.py"

cd ..
set PYTHONPATH=%CD%
cd src
python3 main.py