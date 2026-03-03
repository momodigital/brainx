@echo off
title INSTALASI PREDIKTOR 6 ANGKA - PYTHON
color 0A

echo ================================================
echo    🔷 INSTALASI PREDIKTOR 6 ANGKA - PYTHON
echo ================================================
echo.

:: Cek Python
echo [1/6] Memeriksa instalasi Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python tidak ditemukan!
    echo.
    echo Silakan download Python dari: https://www.python.org/downloads/
    echo PASTikan centang "Add Python to PATH" saat instalasi.
    echo.
    pause
    exit /b
) else (
    for /f "tokens=*" %%i in ('python --version') do echo ✅ %%i
)

:: Cek pip
echo.
echo [2/6] Memeriksa pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip tidak ditemukan!
    echo.
    echo Menginstall pip...
    python -m ensurepip --upgrade
) else (
    for /f "tokens=*" %%i in ('pip --version') do echo ✅ %%i
)

:: Update pip
echo.
echo [3/6] Mengupdate pip ke versi terbaru...
python -m pip install --upgrade pip

:: Install dependencies
echo.
echo [4/6] Menginstall dependencies (numpy, scikit-learn, requests)...
echo.
pip install numpy
pip install scikit-learn
pip install requests

:: Verifikasi instalasi
echo.
echo [5/6] Verifikasi instalasi...
python -c "
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
echo [6/6] Mendownload script prediktor...
curl -o brainx.py https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/brainx.py
curl -o prediktor.py https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/prediktor.py

:: Selesai
echo.
echo ================================================
echo ✅ INSTALASI SELESAI!
echo.
echo 📂 File yang tersedia:
dir brainx.py prediktor.py 2>nul
echo.
echo 🚀 Jalankan dengan perintah:
echo    python prediktor.py
echo.
echo ================================================
pause
