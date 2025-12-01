@echo off

pyinstaller --onefile -w main.py --icon=..\assets\icons\pysee_icon.ico --distpath bin --specpath bin
echo PySee-compile.bat: PROCESS COMPLETED, PRESS ANY KEY TO CLOSE.
set /p UNUSED=""