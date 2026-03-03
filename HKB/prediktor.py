#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 PREDIKTOR 6 ANGKA - MAIN APPLICATION
Versi Final dengan:
✅ Indikator ML tampil di layar
✅ 8 Kepala dan 8 Ekor (peluang 80%)
✅ Bobot Adaptif
✅ Ensemble ML + Statistik
✅ Tanpa auto-check module (untuk Anaconda/PC)
"""

# ========== IMPORT MODULE ==========
import requests
import re
import os
import time
from datetime import datetime

# Import metode dari brainx.py
try:
    from brainx import hitung_semua
except ImportError:
    print("❌ File 'brainx.py' tidak ditemukan!")
    print("Pastikan kedua file berada di folder yang sama:")
    print("  - prediktor.py")
    print("  - brainx.py")
    import sys
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
        lines.append(f"  🤖 ENSEMBLE ADAPTIF (ML:{hasil['ensemble']['ml_weight']*100:.0f}% / STAT:{hasil['ensemble']['stat_weight']*100:.0f}%)")
    lines.append("="*50)
    
    # Info
    lines.append(f"Pasaran: {m_name}")
    lines.append(f"Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lines.append(f"Data: {data_len} putaran")
    if hasil['ensemble']:
        lines.append(f"Confidence ML: {hasil['ensemble']['confidence']:.2%}")
        lines.append(f"Certainty: {hasil['ensemble']['certainty']:.2%}")
        if 'weights' in hasil['ensemble']:
            w = hasil['ensemble']['weights']
            lines.append(f"Bobot Adaptif: Stat={w.get('statistik',0):.0%}, RF={w.get('ml_rf',0):.0%}, LR={w.get('ml_lr',0):.0%}")
    lines.append("")
    
    # Hasil prediksi
    lines.append(f"🔷 6 ANGKA: {'*'.join(map(str, hasil['final']['h6']))}")
    lines.append(f"🏆 3D TOP : {'*'.join(map(str, hasil['final']['h3']))}")
    lines.append("")
    lines.append(f"🎯 8 KEPALA: {'*'.join(map(str, hasil['final']['kepala']))}")
    lines.append(f"🎯 8 EKOR : {'*'.join(map(str, hasil['final']['ekor']))}")
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
    
# 3D Combo - Tampilkan SEMUA di file
if hasil['final']['c3']:
    lines.append("")
    lines.append(f"🎲 3D COMBO ({len(hasil['final']['c3'])}):")
    lines.append("*".join(hasil['final']['c3']))  # ← HAPUS [:200]
    
    # Kepala*Ekor (64 kombinasi)
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
    
    cprint("\n📊 DETAIL MACHINE LEARNING:", Colors.MAGENTA + Colors.BOLD)
    
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
    
    # Tampilkan prediksi ML untuk KEPALA dan EKOR (8 ANGKA)
    if 'kepala_ml' in hasil['ml'] and hasil['ml']['kepala_ml']:
        cprint(f"\n   🎯 PREDIKSI ML UNTUK KEPALA:", Colors.YELLOW)
        cprint(f"        Top 8: {' - '.join(map(str, hasil['ml']['kepala_ml']))}", Colors.WHITE)
    
    if 'ekor_ml' in hasil['ml'] and hasil['ml']['ekor_ml']:
        cprint(f"\n   🎯 PREDIKSI ML UNTUK EKOR:", Colors.YELLOW)
        cprint(f"        Top 8: {' - '.join(map(str, hasil['ml']['ekor_ml']))}", Colors.WHITE)
    
    # Tampilkan prediksi 4 digit lengkap
    prediksi_lengkap = ''.join(map(str, ml_result['predictions']))
    cprint(f"\n   🔢 PREDIKSI 4 DIGIT ML: {Colors.BOLD + Colors.YELLOW}{prediksi_lengkap}{Colors.RESET}", Colors.WHITE)


# ========== FUNGSI TAMPILAN HASIL ==========
def tampilkan_hasil(m_name, data_len, hasil, filter_digits="", f_c2=None):
    """Menampilkan hasil di layar dengan warna"""
    
    cprint("\n" + "="*50, Colors.CYAN)
    cprint(f"🔷 HASIL AKHIR: {m_name}", Colors.BOLD + Colors.MAGENTA)
    
    # Tampilkan indikator ML dengan jelas
    if hasil['ml'] and hasil['ml']['result']:
        # Ada ML
        if hasil['final']['metode'] == 'ensemble':
            cprint(f"🤖 ENSEMBLE ADAPTIF (ML:{hasil['ensemble']['ml_weight']*100:.0f}% / STAT:{hasil['ensemble']['stat_weight']*100:.0f}%)", 
                   Colors.BOLD + Colors.GREEN)
            cprint(f"📊 Confidence ML: {hasil['ensemble']['confidence']:.2%} | Certainty: {hasil['ensemble']['certainty']:.2%}", Colors.CYAN)
            if 'weights' in hasil['ensemble']:
                w = hasil['ensemble']['weights']
                cprint(f"⚖️ Bobot Adaptif: Stat={w.get('statistik',0):.0%}, RF={w.get('ml_rf',0):.0%}, LR={w.get('ml_lr',0):.0%}", Colors.YELLOW)
        else:
            cprint(f"🤖 ML AKTIF (TAPI ENSEMBLE GAGAL)", Colors.BOLD + Colors.YELLOW)
    else:
        # Tidak ada ML
        if hasil['final']['metode'] == 'ensemble':
            cprint("📊 METODE STATISTIK + ENSEMBLE DASAR", Colors.BOLD + Colors.YELLOW)
        else:
            cprint("📊 METODE STATISTIK", Colors.BOLD + Colors.YELLOW)
    
    cprint("="*50, Colors.CYAN)
    
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
    
    # ===== 8 KEPALA & 8 EKOR dengan info ML =====
    cprint(f"\n🎯 8 KEPALA: {Colors.BOLD + Colors.BLUE}{' - '.join(map(str, hasil['final']['kepala']))}{Colors.RESET}", Colors.WHITE)
    if hasil['ml'] and 'kepala_ml' in hasil['ml'] and hasil['ml']['kepala_ml']:
        cprint(f"   🤖 ML rekomendasi: {' - '.join(map(str, hasil['ml']['kepala_ml'][:6]))} ...", Colors.WHITE)

    cprint(f"🎯 8 EKOR : {Colors.BOLD + Colors.RED}{' - '.join(map(str, hasil['final']['ekor']))}{Colors.RESET}", Colors.WHITE)
    if hasil['ml'] and 'ekor_ml' in hasil['ml'] and hasil['ml']['ekor_ml']:
        cprint(f"   🤖 ML rekomendasi: {' - '.join(map(str, hasil['ml']['ekor_ml'][:6]))} ...", Colors.WHITE)
    
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
    if len(c3) <= 50:  # Tetap batasi tampilan layar agar tidak kepanjangan
        cprint("  " + " ".join(c3), Colors.WHITE)
    else:
        cprint("  " + " ".join(c3[:50]) + f" ... ({len(c3)-50} lainnya)", Colors.WHITE)  # Tampilkan 50 di layar
    
    # ===== KEPALA*EKOR (64 kombinasi) =====
    ke = hasil['final']['ke_combo']
    cprint(f"\n💎 KEPALA*EKOR ({Colors.YELLOW}{len(ke)}{Colors.RESET} kombinasi):", Colors.WHITE)
    if len(ke) <= 50:
        cprint("  " + " ".join(ke), Colors.WHITE)
    else:
        cprint("  " + " ".join(ke[:30]) + f" ... ({len(ke)-30} lainnya)", Colors.WHITE)
    
    # ===== TAMPILKAN DETAIL ML =====
    if hasil['ml'] and hasil['ml']['result']:
        tampilkan_hasil_ml(hasil)


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
        # Clear screen (cara yang kompatibel Windows/Linux)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        cprint("\n" + "="*50, Colors.CYAN)
        cprint("   🔷 PREDIKSI ANGKA MAIN - TERMUX EDITION", Colors.BOLD + Colors.CYAN)
        cprint("   💻 Running on PC/Anaconda", Colors.BOLD + Colors.GREEN)
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
        cprint("   3. ❌ Keluar", Colors.WHITE)
        
        try:
            menu = int(input(Colors.GREEN + "\n➤ Pilih menu (1-3): " + Colors.RESET))
        except:
            cprint("❌ Input salah!", Colors.RED)
            input("\nTekan Enter untuk lanjut...")
            continue
        
        if menu == 3:
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
                
                # Buat konten file
                file_content = format_file_output(m_name, len(data), hasil, filt, f_c2)
                
                try:
                    with open(fname, 'w', encoding='utf-8') as f:
                        f.write(file_content)
                    cprint(f"\n✅ Tersimpan di: {Colors.GREEN}{os.path.abspath(fname)}{Colors.RESET}", Colors.WHITE)
                    
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
            import sys
            sys.exit(1)
            
        main()
    except KeyboardInterrupt:
        cprint("\n⚠️ Dibatalkan.", Colors.YELLOW)
    except Exception as e:
        cprint(f"\n❌ Error: {e}", Colors.RED)
