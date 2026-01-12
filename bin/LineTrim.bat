@echo on

call C:\ProgramData\Anaconda3\condabin\conda activate LineTrim
echo Conda activated

cd ..
set PYTHONPATH=%CD%
cd src
python main.py