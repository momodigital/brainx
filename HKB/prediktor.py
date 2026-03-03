#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 PREDIKTOR 6 ANGKA - MAIN APPLICATION
Dengan fitur Validasi dan Bobot Adaptif
"""

# ========== CEK DAN INSTALL MODULE ==========
import subprocess
import sys

def check_and_install_modules():
    """Memeriksa dan menginstall module yang dibutuhkan"""
    required_modules = ['requests', 'numpy', 'scikit-learn']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("="*50)
        print("📦 MODULE YANG DIBUTUHKAN:")
        for module in missing_modules:
            print(f"   - {module}")
        print("="*50)
        
        answer = input("\n💾 Install module sekarang? (y/n): ").lower()
        if answer == 'y':
            for module in missing_modules:
                print(f"📦 Menginstall {module}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            print("✅ Module berhasil diinstall!")
            print("🔄 Silakan jalankan ulang script...")
            sys.exit(0)
        else:
            print("❌ Module tidak diinstall. Script tidak dapat dijalankan.")
            sys.exit(1)

# Jalankan pengecekan module
check_and_install_modules()

# ========== IMPORT MODULE ==========
import requests
import re
import os
import time
from datetime import datetime

# Import metode dari brainx.py
try:
    from brainx import hitung_semua, ModelValidator
except ImportError:
    print("❌ File 'brainx.py' tidak ditemukan!")
    print("Pastikan kedua file berada di folder yang sama:")
    print("  - prediktor.py")
    print("  - brainx.py")
    sys.exit(1)

# ========== KONFIGURASI GITHUB ==========
GITHUB_CONFIG = {
    'username': 'MOMODIGITAL',
    'repo': 'data-vault',
    'branch': 'main',
    'path': 'data'
}

MARKET_FILES = {
    1: ('magnum-cambodia', 'magnum-cambodia.csv'),
    2: ('sydney-pools', 'sydney-pools.csv'),
    3: ('sydney-lotto', 'sydney-lotto.csv'),
    4: ('china-pools', 'china-pools.csv'),
    5: ('singapore', 'singapore.csv'),
    6: ('taiwan', 'taiwan.csv'),
    7: ('hongkong-pools', 'hongkong-pools.csv'),
    8: ('hongkong-lotto', 'hongkong-lotto.csv'),
    9: ('newyork-evening', 'newyork-evening.csv'),
    10: ('kentucky-evening', 'kentucky-evening.csv')
}

MARKET_NAMES = {
    1: 'Magnum Cambodia',
    2: 'Sydney Pools',
    3: 'Sydney Lotto',
    4: 'China Pools',
    5: 'Singapore',
    6: 'Taiwan',
    7: 'Hongkong Pools',
    8: 'Hongkong Lotto',
    9: 'New York Evening',
    10: 'Kentucky Evening'
}

# ========== WARNA ANSI ==========
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

def cprint(text, color=Colors.RESET):
    print(f"{color}{text}{Colors.RESET}")

# ========== FUNGSI FETCH DATA ==========
def fetch_github_csv(market_key):
    file_info = MARKET_FILES.get(market_key)
    if not file_info:
        return None
    url = f"https://raw.githubusercontent.com/{GITHUB_CONFIG['username']}/{GITHUB_CONFIG['repo']}/{GITHUB_CONFIG['branch']}/{GITHUB_CONFIG['path']}/{file_info[1]}"
    try:
        cprint("📡 Mengambil data dari Database...", Colors.CYAN)
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.text
    except Exception as e:
        cprint(f"❌ Error: {e}", Colors.RED)
        return None

# ========== FUNGSI PARSE CSV ==========
def parse_csv(text):
    if not text:
        return [], []
    results, dates = [], []
    for line in text.strip().split('\n')[1:]:
        if not line:
            continue
        parts = line.split(',')
        if len(parts) >= 2:
            match = re.search(r'\d{4}', parts[1].strip())
            if match:
                dates.append(parts[0].strip())
                results.append(match.group())
    return results, dates

# ========== FUNGSI FILTER ==========
def filter_2d(c2, filter_digits):
    """Filter 2D berdasarkan digit yang diinginkan"""
    if not filter_digits:
        return c2
    digits = [int(x) for x in filter_digits if x.isdigit()]
    return [x for x in c2 if any(int(c) in digits for c in x)]

# ========== FUNGSI FORMAT OUTPUT UNTUK FILE ==========
def format_file_output(m_name, data_len, hasil, filter_digits, f_c2):
    """Membuat string output untuk file dengan pemisah *"""
    lines = []
    
    # Header
    lines.append("="*50)
    lines.append("  🔷 PREDIKTOR 6 ANGKA - HASIL LENGKAP")
    if hasil['final']['metode'] == 'ensemble':
        lines.append(f"  🤖 ENSEMBLE ADAPTIF (ML:{(hasil['ensemble']['ml_weight']*100):.0f}% / STAT:{hasil['ensemble']['stat_weight']*100:.0f}%)")
    lines.append("="*50)
    
    # Info
    lines.append(f"Pasaran: {m_name}")
    lines.append(f"Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lines.append(f"Data: {data_len} putaran")
    if hasil['ensemble']:
        lines.append(f"Confidence ML: {hasil['ensemble']['confidence']:.2%}")
        lines.append(f"Certainty: {hasil['ensemble']['certainty']:.2%}")
        # Tampilkan bobot adaptif
        if 'weights' in hasil['ensemble']:
            weights = hasil['ensemble']['weights']
            lines.append(f"Bobot Adaptif: Stat={weights.get('statistik',0):.0%}, RF={weights.get('ml_rf',0):.0%}, LR={weights.get('ml_lr',0):.0%}")
    lines.append("")
    
    # Hasil prediksi
    lines.append(f"🔷 6 ANGKA: {'*'.join(map(str, hasil['final']['h6']))}")
    lines.append(f"🏆 3D TOP : {'*'.join(map(str, hasil['final']['h3']))}")
    lines.append("")
    lines.append(f"🎯 7 KEPALA: {'*'.join(map(str, hasil['final']['kepala']))}")
    lines.append(f"🎯 7 EKOR : {'*'.join(map(str, hasil['final']['ekor']))}")
    lines.append("")
    
    # 2D
    lines.append(f"🔢 2D AUTO ({len(hasil['final']['c2'])}):")
    lines.append("*".join(hasil['final']['c2']))
    
    # Filter
    if filter_digits:
        lines.append("")
        lines.append(f"✂️ FILTER {filter_digits}: {len(f_c2)} dari {len(hasil['final']['c2'])}")
        if f_c2:
            lines.append("*".join(f_c2))
    
    # 3D Combo
    if hasil['final']['c3']:
        lines.append("")
        lines.append(f"🎲 3D COMBO ({len(hasil['final']['c3'])}):")
        lines.append("*".join(hasil['final']['c3']))
    
    # Kepala*Ekor
    lines.append("")
    lines.append(f"💎 KEPALA*EKOR ({len(hasil['final']['ke_combo'])}):")
    lines.append("*".join(hasil['final']['ke_combo']))
    
    # Footer
    lines.append("")
    lines.append("="*50)
    lines.append("Gunakan dengan bijak. Good luck! 🍀")
    
    return "\n".join(lines)

# ========== FUNGSI TAMPILAN HASIL ML ==========
def tampilkan_hasil_ml(hasil):
    """Menampilkan detail hasil Machine Learning"""
    if not hasil['ml'] or not hasil['ml']['result']:
        return
    
    ml_result = hasil['ml']['result']
    
    cprint("\n📊 DETAIL MACHINE LEARNING (ANTI-OVERFITTING):", Colors.MAGENTA + Colors.BOLD)
    
    # Tampilkan Cross Validation scores
    if ml_result.get('cv_scores'):
        cprint("   Cross Validation Scores:", Colors.CYAN)
        for i, cv in enumerate(ml_result['cv_scores']):
            posisi = ['Ribuan', 'Ratusan', 'Puluhan', 'Satuan'][i]
            cprint(f"     {posisi}: RF={cv['rf']:.2%}, LR={cv['lr']:.2%}, GB={cv['gb']:.2%} (Best: {cv['best']})", Colors.WHITE)
    
    # Tampilkan akurasi per posisi
    cprint("   Akurasi Model per Posisi (CV mean):", Colors.CYAN)
    for i, acc in enumerate(ml_result['accuracies']):
        posisi = ['Ribuan', 'Ratusan', 'Puluhan', 'Satuan'][i]
        cprint(f"     {posisi}: {acc:.2%}", Colors.WHITE)
    
    # Tampilkan confidence dan certainty
    cprint(f"   Confidence Score: {ml_result['confidence']:.2%}", Colors.GREEN)
    cprint(f"   Certainty (1-Entropy): {ml_result['certainty']:.2%}", Colors.CYAN)
    
    # Tampilkan prediksi ML untuk setiap posisi
    cprint("\n   🎯 PREDIKSI ML PER POSISI:", Colors.YELLOW)
    
    for i in range(4):
        posisi = ['RIBUAAN', 'RATUSAN', 'PULUHAN', 'SATUAN'][i]
        pred = ml_result['predictions'][i]
        prob = ml_result['probabilities'][i]
        
        # Tampilkan top 5 digit untuk posisi ini
        top_digits = ml_result['top_digits'][i][:5]
        
        cprint(f"     {posisi}: {Colors.BOLD}{pred}{Colors.RESET} (prob: {prob:.2%})", Colors.WHITE)
        cprint(f"        Top 5: {' - '.join(map(str, top_digits))}", Colors.WHITE)
    
    # Tampilkan prediksi 4 digit lengkap
    prediksi_lengkap = ''.join(map(str, ml_result['predictions']))
    cprint(f"\n   🔢 PREDIKSI 4 DIGIT ML: {Colors.BOLD + Colors.YELLOW}{prediksi_lengkap}{Colors.RESET}", Colors.WHITE)


def tampilkan_hasil(m_name, data_len, hasil, filter_digits="", f_c2=None):
    """Menampilkan hasil di layar dengan warna"""
    
    cprint("\n" + "="*50, Colors.CYAN)
    cprint(f"🔷 HASIL AKHIR: {m_name}", Colors.BOLD + Colors.MAGENTA)
    
    if hasil['final']['metode'] == 'ensemble':
        # Header dengan bobot adaptif
        cprint(f"🤖 ENSEMBLE ADAPTIF", Colors.BOLD + Colors.GREEN)
        
        # Baris 1: Bobot dan Confidence
        ml_persen = hasil['ensemble']['ml_weight']*100
        stat_persen = hasil['ensemble']['stat_weight']*100
        cprint(f"📊 Bobot: ML {ml_persen:.0f}% | STAT {stat_persen:.0f}%", Colors.CYAN)
        
        # Baris 2: Confidence & Certainty
        cprint(f"📈 Confidence: {hasil['ensemble']['confidence']:.2%} | Certainty: {hasil['ensemble']['certainty']:.2%}", Colors.YELLOW)
        
        # Baris 3: Detail bobot per metode (jika ada)
        if 'weights' in hasil['ensemble']:
            w = hasil['ensemble']['weights']
            stat = w.get('statistik', 0) * 100
            rf = w.get('ml_rf', 0) * 100
            lr = w.get('ml_lr', 0) * 100
            
            # Dapatkan angka dari masing-masing metode
            stat_angka = ' '.join(map(str, hasil['statistik']['h6']['h6'][:3])) + "..."
            
            ml_angka = ""
            if hasil['ml'] and hasil['ml']['result']:
                ml_pred = ''.join(map(str, hasil['ml']['result']['predictions']))
                ml_angka = f"ML:{ml_pred}"
            else:
                ml_angka = "ML:?"
            
            ensemble_angka = ' '.join(map(str, hasil['final']['h6']))
            
            cprint(f"⚖️  Bobot Detail:", Colors.MAGENTA)
            cprint(f"   📊 Stat {stat:.0f}% : {stat_angka}", Colors.WHITE)
            cprint(f"   🤖 RF   {rf:.0f}% : {ml_angka}", Colors.WHITE)
            cprint(f"   📈 LR   {lr:.0f}% : {ml_angka}", Colors.WHITE)
            cprint(f"   🔮 Ensemble : {Colors.BOLD}{ensemble_angka}{Colors.RESET}", Colors.GREEN)
    else:
        cprint("📊 METODE STATISTIK", Colors.BOLD + Colors.YELLOW)
    
    cprint("="*50, Colors.CYAN)
    
    # Sisanya sama...
    # [kode selanjutnya tidak berubah]
    
    # ===== HASIL UTAMA =====
    cprint(f"\n🔷 6 ANGKA: {Colors.BOLD + Colors.YELLOW}{' - '.join(map(str, hasil['final']['h6']))}{Colors.RESET}", Colors.WHITE)
    cprint(f"🏆 3D TOP : {Colors.BOLD + Colors.GREEN}{' - '.join(map(str, hasil['final']['h3']))}{Colors.RESET}", Colors.WHITE)
    
    # ===== PERBANDINGAN METODE =====
    cprint(f"\n📊 PERBANDINGAN METODE:", Colors.CYAN)
    
    # Statistik
    cprint(f"   📈 Statistik : {Colors.YELLOW}{' - '.join(map(str, hasil['statistik']['h6']['h6']))}{Colors.RESET}", Colors.WHITE)
    
    # ML (jika ada)
    if hasil['ml'] and hasil['ml']['result']:
        ml_result = hasil['ml']['result']
        ml_digits = []
        for pos in range(4):
            if ml_result['top_digits'][pos]:
                ml_digits.append(str(ml_result['top_digits'][pos][0]))
            else:
                ml_digits.append('?')
        cprint(f"   🤖 ML Only   : {Colors.MAGENTA}{' - '.join(ml_digits)}{Colors.RESET} (conf: {ml_result['confidence']:.2%})", Colors.WHITE)
        
        # Tampilkan prediksi 4 digit ML
        if ml_result['predictions']:
            pred_4d = ''.join(map(str, ml_result['predictions']))
            cprint(f"   🎯 ML 4D     : {Colors.BOLD + Colors.CYAN}{pred_4d}{Colors.RESET}", Colors.WHITE)
    
    # Ensemble
    if hasil['ensemble']:
        ensemble_h6 = ' - '.join(map(str, hasil['ensemble']['h6']['h6']))
        cprint(f"   🔮 Ensemble  : {Colors.BOLD + Colors.GREEN}{ensemble_h6}{Colors.RESET}", Colors.WHITE)
    
    # ===== KEPALA & EKOR =====
    cprint(f"\n🎯 7 KEPALA: {Colors.BOLD + Colors.BLUE}{' - '.join(map(str, hasil['final']['kepala']))}{Colors.RESET}", Colors.WHITE)
    cprint(f"🎯 7 EKOR : {Colors.BOLD + Colors.RED}{' - '.join(map(str, hasil['final']['ekor']))}{Colors.RESET}", Colors.WHITE)
    
    # ===== 2D =====
    c2 = hasil['final']['c2']
    cprint(f"\n🔢 2D AUTO ({Colors.CYAN}{len(c2)}{Colors.RESET} kombinasi):", Colors.WHITE)
    if len(c2) <= 50:
        cprint("  " + " ".join(c2), Colors.WHITE)
    else:
        cprint("  " + " ".join(c2[:30]) + f" ... ({len(c2)-30} lainnya)", Colors.WHITE)
    
    # ===== FILTER =====
    if filter_digits and f_c2 is not None:
        cprint(f"\n✂️ Setelah Filter {filter_digits}: {Colors.RED}{len(f_c2)}{Colors.RESET} dari {Colors.CYAN}{len(c2)}{Colors.RESET}", Colors.WHITE)
        if len(f_c2) > 0:
            if len(f_c2) <= 50:
                cprint("  " + " ".join(f_c2), Colors.WHITE)
            else:
                cprint("  " + " ".join(f_c2[:30]) + f" ... ({len(f_c2)-30} lainnya)", Colors.WHITE)
    
    # ===== 3D COMBO =====
    if hasil['final']['c3']:
        c3 = hasil['final']['c3']
        cprint(f"\n🎲 3D COMBO ({Colors.MAGENTA}{len(c3)}{Colors.RESET} kombinasi):", Colors.WHITE)
        if len(c3) <= 50:
            cprint("  " + " ".join(c3), Colors.WHITE)
        else:
            cprint("  " + " ".join(c3[:30]) + f" ... ({len(c3)-30} lainnya)", Colors.WHITE)
    
    # ===== KEPALA*EKOR =====
    ke = hasil['final']['ke_combo']
    cprint(f"\n💎 KEPALA*EKOR ({Colors.YELLOW}{len(ke)}{Colors.RESET} kombinasi):", Colors.WHITE)
    if len(ke) <= 50:
        cprint("  " + " ".join(ke), Colors.WHITE)
    else:
        cprint("  " + " ".join(ke[:30]) + f" ... ({len(ke)-30} lainnya)", Colors.WHITE)
    
    # ===== TAMPILKAN DETAIL ML =====
    if hasil['ml'] and hasil['ml']['result']:
        tampilkan_hasil_ml(hasil)


# ========== FUNGSI VALIDASI ==========
def menu_validasi(data):
    """Menu untuk menjalankan validasi akurasi"""
    if len(data) < 60:
        cprint("❌ Data terlalu sedikit untuk validasi (minimal 60 putaran)", Colors.RED)
        return
    
    cprint("\n" + "="*50, Colors.CYAN)
    cprint("📊 VALIDASI AKURASI METODE", Colors.BOLD + Colors.YELLOW)
    cprint("="*50, Colors.CYAN)
    
    methods_to_validate = {
        '6 ANGKA': lambda d: calc6(d)['h6'],
        '3D TOP': lambda d: calc3(d)['h3'],
        'KEPALA': calc_kepala,
        'EKOR': calc_ekor
    }
    
    # Import ulang fungsi dari brainx
    from brainx import calc6, calc3, calc_kepala, calc_ekor
    
    results = ModelValidator.compare_methods(data, methods_to_validate)
    
    # Urutkan berdasarkan mean accuracy
    sorted_methods = sorted(results.items(), 
                           key=lambda x: x[1]['mean_accuracy'], 
                           reverse=True)
    
    for name, result in sorted_methods:
        trend_symbol = "📈" if result['trend'] > 0 else "📉" if result['trend'] < 0 else "➡️"
        cprint(f"\n{name}:", Colors.BOLD + Colors.WHITE)
        cprint(f"  Mean Accuracy : {Colors.GREEN}{result['mean_accuracy']:.2%}{Colors.RESET} {trend_symbol}", Colors.WHITE)
        cprint(f"  Std Deviation : {result['std_accuracy']:.2%}", Colors.WHITE)
        cprint(f"  Last 10 Acc   : {Colors.YELLOW}{result['last_10_accuracy']:.2%}{Colors.RESET}", Colors.WHITE)
        cprint(f"  Total Tests   : {result['total_tests']}", Colors.WHITE)
        
        # Tampilkan sample prediksi
        if result['predictions']:
            cprint("  Sample Prediksi (5 terakhir):", Colors.CYAN)
            for i, (pred, actual) in enumerate(zip(result['predictions'][-5:], 
                                                   result['actuals'][-5:])):
                if isinstance(pred, list):
                    pred_str = ' '.join(map(str, pred[:3])) + "..."
                else:
                    pred_str = str(pred)
                cprint(f"    {i+1}. Pred: {pred_str} | Aktual: {actual}", Colors.WHITE)


# ========== FUNGSI MENU KONFIGURASI ==========
def menu_konfigurasi():
    """Menu untuk mengatur bobot ML"""
    cprint("\n⚙️ KONFIGURASI ML ADAPTIF", Colors.CYAN)
    cprint("1. Mode Adaptif (bobot otomatis berdasarkan performa)", Colors.WHITE)
    cprint("2. Bobot Manual: 60% ML (default)", Colors.WHITE)
    cprint("3. Bobot Manual: 70% ML", Colors.WHITE)
    cprint("4. Bobot Manual: 50% ML", Colors.WHITE)
    cprint("5. Bobot Manual: 40% ML", Colors.WHITE)
    cprint("6. Bobot Manual: 80% ML", Colors.WHITE)
    cprint("7. Matikan ML (statistik only)", Colors.WHITE)
    cprint("0. Kembali", Colors.WHITE)
    
    try:
        pilihan = int(input(Colors.GREEN + "\n➤ Pilih (0-7): " + Colors.RESET))
        if pilihan == 1:
            return 'adaptive', 0.6
        elif pilihan == 2:
            return 'manual', 0.6
        elif pilihan == 3:
            return 'manual', 0.7
        elif pilihan == 4:
            return 'manual', 0.5
        elif pilihan == 5:
            return 'manual', 0.4
        elif pilihan == 6:
            return 'manual', 0.8
        elif pilihan == 7:
            return 'off', 0
        else:
            return None, None
    except:
        return None, None

# ========== FUNGSI UTAMA ==========
def main():
    # Default konfigurasi
    ml_mode = 'adaptive'  # 'adaptive', 'manual', 'off'
    ml_weight = 0.6
    optimizer = None  # Akan diisi oleh brainx
    
    while True:
        os.system('clear')
        
        cprint("\n" + "="*50, Colors.CYAN)
        cprint("   🔷 PREDIKSI ANGKA MAIN - TERMUX", Colors.BOLD + Colors.CYAN)
        if ml_mode == 'adaptive':
            cprint("   🤖 ML ADAPTIF (bobot otomatis)", Colors.BOLD + Colors.GREEN)
        elif ml_mode == 'manual':
            cprint(f"   🤖 ML MANUAL ({ml_weight*100:.0f}% bobot)", Colors.BOLD + Colors.YELLOW)
        else:
            cprint("   📊 STATISTIK ONLY", Colors.BOLD + Colors.RED)
        cprint("="*50, Colors.CYAN)
        
        cprint("\n📋 MENU UTAMA:", Colors.YELLOW)
        cprint("   1. 🔍 Prediksi Pasaran", Colors.WHITE)
        cprint("   2. ⚙️  Konfigurasi ML", Colors.WHITE)
        cprint("   3. 📊 Validasi Akurasi", Colors.WHITE)
        cprint("   4. ❌ Keluar", Colors.WHITE)
        
        try:
            menu = int(input(Colors.GREEN + "\n➤ Pilih menu (1-4): " + Colors.RESET))
        except:
            cprint("❌ Input salah!", Colors.RED)
            input("\nTekan Enter untuk lanjut...")
            continue
        
        if menu == 4:
            cprint("\n👋 Sampai jumpa!", Colors.CYAN)
            break
            
        elif menu == 2:
            baru_mode, baru_weight = menu_konfigurasi()
            if baru_mode is not None:
                ml_mode = baru_mode
                ml_weight = baru_weight if baru_weight else 0.6
                if ml_mode == 'adaptive':
                    cprint("✅ Mode Adaptif diaktifkan! Bobot akan menyesuaikan otomatis.", Colors.GREEN)
                else:
                    cprint("✅ Konfigurasi tersimpan!", Colors.GREEN)
            input("\nTekan Enter untuk lanjut...")
            continue
            
        elif menu == 3:
            # Minta user pilih pasaran untuk validasi
            cprint("\n📊 PILIH PASARAN UNTUK VALIDASI:", Colors.YELLOW)
            for k, v in MARKET_NAMES.items():
                cprint(f"   {k}. {v}", Colors.WHITE)
            
            try:
                choice = int(input(Colors.GREEN + "\n➤ Nomor Pasaran (1-10): " + Colors.RESET))
                if choice not in MARKET_FILES:
                    raise ValueError
            except:
                cprint("❌ Input salah!", Colors.RED)
                input("\nTekan Enter untuk lanjut...")
                continue
            
            m_name = MARKET_NAMES[choice]
            cprint(f"\n🔄 Loading {m_name} untuk validasi...", Colors.CYAN)
            
            csv = fetch_github_csv(choice)
            if not csv:
                cprint("❌ Gagal ambil data.", Colors.RED)
                input("\nTekan Enter untuk lanjut...")
                continue
            
            data, _ = parse_csv(csv)
            menu_validasi(data)
            input("\nTekan Enter untuk kembali ke menu...")
            continue
            
        elif menu == 1:
            # Tampilkan pilihan pasaran
            cprint("\n📊 PILIH PASARAN:", Colors.YELLOW)
            for k, v in MARKET_NAMES.items():
                cprint(f"   {k}. {v}", Colors.WHITE)
            
            try:
                choice = int(input(Colors.GREEN + "\n➤ Nomor Pasaran (1-10): " + Colors.RESET))
                if choice not in MARKET_FILES:
                    raise ValueError
            except:
                cprint("❌ Input salah!", Colors.RED)
                input("\nTekan Enter untuk lanjut...")
                continue

            m_name = MARKET_NAMES[choice]
            cprint(f"\n🔄 Loading {m_name}...", Colors.CYAN)
            
            # Ambil data
            csv = fetch_github_csv(choice)
            if not csv:
                cprint("❌ Gagal ambil data. Cek internet!", Colors.RED)
                input("\nTekan Enter untuk lanjut...")
                continue
            
            data, _ = parse_csv(csv)
            if len(data) < 15:
                cprint(f"❌ Data kurang ({len(data)}). Minimal 15.", Colors.RED)
                input("\nTekan Enter untuk lanjut...")
                continue
            
            cprint(f"✅ Data: {len(data)} putaran. Memproses...", Colors.GREEN)
            time.sleep(1)
            
            # Hitung semua metode
            cprint("\n📊 Menjalankan semua metode prediksi...", Colors.CYAN)
            
            use_ml = ml_mode != 'off'
            if ml_mode == 'adaptive':
                # Mode adaptif: gunakan optimizer dari iterasi sebelumnya
                hasil = hitung_semua(data, use_ml=use_ml, ml_weight=ml_weight, 
                                    optimizer=optimizer, verbose=True)
                if hasil['optimizer']:
                    optimizer = hasil['optimizer']
            else:
                # Mode manual: bobot tetap
                hasil = hitung_semua(data, use_ml=use_ml, ml_weight=ml_weight, 
                                    verbose=True)
            
            # Filter
            filt = input(Colors.YELLOW + "\n🔧 Filter digit (contoh: 159) / Enter skip: " + Colors.RESET).strip()
            f_c2 = filter_2d(hasil['final']['c2'], filt) if filt else hasil['final']['c2']
            
            # Tampilkan hasil
            tampilkan_hasil(m_name, len(data), hasil, filt, f_c2)
            
            # Simpan file
            save = input(Colors.GREEN + "\n💾 Simpan ke file? (y/n): " + Colors.RESET).lower()
            if save == 'y':
                # Buat nama file
                mode = "adaptif" if ml_mode == 'adaptive' else "manual" if ml_mode == 'manual' else "stat"
                fname = f"prediktor_{mode}_{choice}_{datetime.now().strftime('%H%M%S')}.txt"
                
                # Tentukan path
                if os.path.exists('/sdcard'):
                    download_dir = '/sdcard/Download'
                    if not os.path.exists(download_dir):
                        download_dir = '/sdcard'
                    path = os.path.join(download_dir, fname)
                else:
                    path = fname
                
                # Buat konten file
                file_content = format_file_output(m_name, len(data), hasil, filt, f_c2)
                
                try:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(file_content)
                    cprint(f"\n✅ Tersimpan di: {Colors.GREEN}{path}{Colors.RESET}", Colors.WHITE)
                    
                    # Pratinjau
                    cprint("\n📄 Pratinjau (5 baris pertama):", Colors.CYAN)
                    preview = file_content.split('\n')[:5]
                    for line in preview:
                        print(line)
                    print("...")
                    
                except Exception as e:
                    cprint(f"\n❌ Gagal menyimpan: {e}", Colors.RED)
            
            input(Colors.CYAN + "\nTekan Enter untuk kembali ke menu..." + Colors.RESET)

# ========== ENTRY POINT ==========
if __name__ == "__main__":
    try:
        # Cek ketersediaan file brainx
        if not os.path.exists('brainx.py'):
            cprint("\n❌ ERROR: File 'brainx.py' tidak ditemukan!", Colors.RED)
            cprint("Pastikan kedua file berada di folder yang sama:", Colors.YELLOW)
            cprint("  - prediktor.py", Colors.WHITE)
            cprint("  - brainx.py", Colors.WHITE)
            sys.exit(1)
            
        main()
    except KeyboardInterrupt:
        cprint("\n⚠️ Dibatalkan.", Colors.YELLOW)
    except Exception as e:
        cprint(f"\n❌ Error: {e}", Colors.RED)
