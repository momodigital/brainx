# install_pc.py
import subprocess
import sys
import os

def main():
    print("="*50)
    print("  🔷 INSTALL PREDIKTOR UNTUK PC")
    print("="*50)
    
    # Cek Python version
    print(f"\n📌 Python version: {sys.version}")
    
    # Install dependencies
    print("\n📦 Menginstall dependencies...")
    packages = ['numpy', 'scikit-learn', 'requests']
    
    for package in packages:
        print(f"   Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    # Download script
    print("\n📥 Download script...")
    import requests
    
    files = {
        'brainx.py': 'https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/brainx.py',
        'prediktor.py': 'https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/prediktor.py'
    }
    
    for filename, url in files.items():
        print(f"   Downloading {filename}...")
        r = requests.get(url)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(r.text)
    
    # Verifikasi
    print("\n🔍 Verifikasi instalasi...")
    try:
        import numpy
        import sklearn
        import requests
        print("✅ Semua package berhasil diimport!")
        print(f"   numpy: {numpy.__version__}")
        print(f"   scikit-learn: {sklearn.__version__}")
        print(f"   requests: {requests.__version__}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("\n" + "="*50)
    print("✅ INSTALASI SELESAI!")
    print("📂 File tersedia:")
    os.system("ls -la brainx.py prediktor.py 2>nul || dir brainx.py prediktor.py")
    print("\n🚀 Jalankan: python prediktor.py")
    print("="*50)

if __name__ == "__main__":
    main()
