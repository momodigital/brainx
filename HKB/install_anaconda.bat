@echo off
title INSTALASI PREDIKTOR 6 ANGKA - ANACONDA
color 0A

echo ================================================
echo    🔷 INSTALASI PREDIKTOR 6 ANGKA - ANACONDA
echo ================================================
echo.

:: Cek conda
echo [1/7] Memeriksa instalasi Anaconda/Miniconda...
conda --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Conda tidak ditemukan!
    echo.
    echo Silakan install Anaconda dari: https://www.anaconda.com/download
    echo Atau Miniconda dari: https://docs.conda.io/en/latest/miniconda.html
    echo.
    pause
    exit /b
) else (
    for /f "tokens=*" %%i in ('conda --version') do echo ✅ %%i
)

:: Tanya nama environment
echo.
set /p env_name="Masukkan nama environment (default: prediktor): "
if "%env_name%"=="" set env_name=prediktor

:: Buat environment
echo.
echo [2/7] Membuat environment %env_name% dengan Python 3.11...
conda create -y -n %env_name% python=3.11

:: Aktifkan environment
echo.
echo [3/7] Mengaktifkan environment...
call conda activate %env_name% 2>nul

:: Install dependencies via conda
echo.
echo [4/7] Menginstall dependencies via conda (numpy, scikit-learn)...
conda install -y -n %env_name% numpy scikit-learn

:: Install requests via pip
echo.
echo [5/7] Menginstall requests via pip...
conda run -n %env_name% pip install requests

:: Verifikasi instalasi
echo.
echo [6/7] Verifikasi instalasi...
conda run -n %env_name% python -c "
import sys
print(f'✅ Python: {sys.version}')
try:
    import numpy
    print(f'✅ numpy: {numpy.__version__}')
except: print('❌ numpy error')
try:
    import sklearn
    print(f'✅ scikit-learn: {sklearn.__version__}')
except: print('❌ scikit-learn error')
try:
    import requests
    print(f'✅ requests: {requests.__version__}')
except: print('❌ requests error')
"

:: Download script
echo.
echo [7/7] Mendownload script prediktor...
curl -o brainx.py https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/brainx.py
curl -o prediktor.py https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/prediktor.py

:: Buat file activator
echo.
echo Membuat file activator...
(
echo @echo off
echo echo Mengaktifkan environment %env_name%...
echo call conda activate %env_name%
echo echo.
echo echo 🔷 Menjalankan prediktor...
echo python prediktor.py
) > run_prediktor.bat

:: Selesai
echo.
echo ================================================
echo ✅ INSTALASI SELESAI!
echo.
echo 📂 File yang tersedia:
dir brainx.py prediktor.py run_prediktor.bat 2>nul
echo.
echo 🚀 Cara menjalankan:
echo   1. Double-click run_prediktor.bat
echo   2. Atau manual:
echo      conda activate %env_name%
echo      python prediktor.py
echo.
echo ================================================
pause
