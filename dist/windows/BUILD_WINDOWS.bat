@echo off
REM How to produce a self-contained Windows installer (.exe):

REM Step 1: bundle installer script & README on a Windows machine
REM Step 2: run from an elevated PowerShell:
powershell -NoProfile -Command "& { Remove-Item -Recurse -Force dist }; git clone https://github.com/tarri-dev/tarri dist; cd dist; bash build_tarri_packages.sh; pyinstaller --onefile --name tarri.exe --noconfirm --clean; ren build\\tarri.exe dist\\windows\\tarri.exe"
