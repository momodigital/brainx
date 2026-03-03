# 🔷 PREDIKTOR 6 ANGKA - Termux Edition
Metode BrainX Investasi Haram
![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![ML](https://img.shields.io/badge/ML-Random%20Forest%20%7C%20Logistic%20Regression-orange)
![Platform](https://img.shields.io/badge/platform-Termux-red)

**Prediktor 6 Angka** adalah aplikasi prediksi angka togel berbasis Termux yang menggabungkan **metode statistik** dan **machine learning** dengan sistem **bobot adaptif** dan **anti-overfitting**. Data diambil langsung dari repository GitHub.

## 📋 DAFTAR ISI
- [Fitur Utama](#fitur-utama)
- [Screenshot](#screenshot)
- [Cara Install](#cara-install)
- [Cara Penggunaan](#cara-penggunaan)
- [Metode Prediksi](#metode-prediksi)
- [Machine Learning](#machine-learning)
- [Validasi Akurasi](#validasi-akurasi)
- [Struktur File](#struktur-file)
- [Troubleshooting](#troubleshooting)
- [Lisensi](#lisensi)

---

## 🎯 FITUR UTAMA

### ✅ Metode Statistik Lengkap
- **6 ANGKA** - Analisis frekuensi, posisi, dan pola 2D
- **3D TOP** - Analisis dengan time decay dan gap analysis
- **7 KEPALA** - Fokus pada posisi puluhan
- **7 EKOR** - Fokus pada posisi satuan
- **2D AUTO** - Generate semua kombinasi 2D
- **3D COMBO** - Generate kombinasi 3D
- **KEPALA*EKOR** - Kombinasi kepala dan ekor

### 🤖 Machine Learning
- **Random Forest Classifier** dengan regularization
- **Logistic Regression** dengan L2 penalty
- **Gradient Boosting** sebagai alternatif
- **Cross Validation** (TimeSeriesSplit)
- **Feature Extraction** 66 fitur dari data historis
- **Anti-overfitting** dengan max_depth, min_samples_split, dll

### 📊 Bobot Adaptif
- Bobot **otomatis menyesuaikan** berdasarkan performa
- 3 komponen bobot: Statistik, Random Forest, Logistic Regression
- **Memory decay** - data terbaru berbobot lebih besar
- Tampil transparan di layar

### 🔍 Validasi Akurasi
- **Backtesting** dengan data historis
- **Mean accuracy** setiap metode
- **Trend analysis** (naik/turun)
- **Sample prediksi** vs aktual
- Menu khusus validasi

### 📱 Termux Optimization
- **Warna ANSI** untuk tampilan menarik
- **Penyimpanan otomatis** ke /sdcard/Download
- **Filter digit** interaktif
- **Pratinjau file** setelah disimpan

---

## 📸 SCREENSHOT

```

==================================================
🔷 PREDIKSI ANGKA MAIN - TERMUX
🤖 ML ADAPTIF (bobot otomatis)
==================================================

📋 MENU UTAMA:

1. 🔍 Prediksi Pasaran
2. ⚙️ Konfigurasi ML
3. 📊 Validasi Akurasi
4. ❌ Keluar

➤ Pilih menu (1-4):

```

**Hasil Prediksi:**
```

==================================================
🔷 HASIL AKHIR: Singapore
🤖 ENSEMBLE ADAPTIF
📊 Bobot: ML 65% | STAT 35%
📈 Confidence: 73.45% | Certainty: 68.23%
⚖️ Bobot Detail:
📊 Stat 35% : 3 7 1 ...
🤖 RF   42% : ML:7351
📈 LR   23% : ML:7351
🔮 Ensemble : 3 7 1 5 9 2
==================================================

🔷 6 ANGKA: 3 - 7 - 1 - 5 - 9 - 2
🏆 3D TOP : 7 - 3 - 9
...

```

---

## 🚀 CARA INSTALL

### Metode 1: Auto Install (Rekomendasi)
```bash
# Copy paste semua ini ke Termux:
pkg update -y && pkg install python python-pip -y && \
curl -o brainx.py https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/brainx.py && \
curl -o prediktor.py https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/prediktor.py && \
pip install requests numpy scikit-learn && \
python prediktor.py
```

Metode 2: Manual Step-by-Step

```bash
# 1. Update package
pkg update && pkg upgrade

# 2. Install Python
pkg install python python-pip

# 3. Download script
curl -o brainx.py https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/brainx.py
curl -o prediktor.py https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/prediktor.py

# 4. Install dependencies
pip install requests numpy scikit-learn

# 5. Jalankan
python prediktor.py
```

Metode 3: Download Script Installer

```bash
# Buat file installer
nano install_prediktor.sh

# Paste kode installer, lalu jalankan
chmod +x install_prediktor.sh
./install_prediktor.sh
```

---

📖 CARA PENGGUNAAN

Menu Utama

```
1. 🔍 Prediksi Pasaran - Jalankan prediksi untuk pasaran tertentu
2. ⚙️ Konfigurasi ML - Atur mode ML (adaptif/manual/mati)
3. 📊 Validasi Akurasi - Lihat performa metode pada data historis
4. ❌ Keluar - Tutup program
```

Prediksi Pasaran

```
📊 PILIH PASARAN:
   1. Magnum Cambodia
   2. Sydney Pools
   3. Sydney Lotto
   4. China Pools
   5. Singapore
   6. Taiwan
   7. Hongkong Pools
   8. Hongkong Lotto
   9. New York Evening
   10. Kentucky Evening

➤ Nomor Pasaran (1-10): 5
```

Filter Digit

```
🔧 Filter digit (contoh: 159) / Enter skip: 159
✂️ Setelah Filter 159: 42 dari 78
  01 05 09 10 11 12 13 14 15 16 ... (32 lainnya)
```

Simpan Hasil

```
💾 Simpan ke file? (y/n): y
✅ Tersimpan di: /sdcard/Download/prediktor_adaptif_5_143022.txt
```

---

🧠 METODE PREDIKSI

1. Metode Statistik

Metode Deskripsi Bobot
6 ANGKA Analisis frekuensi semua digit + posisi + pola 2D 20-25 poin
3D TOP Time decay (0.98^n) + gap analysis + posisi 25-30 poin
KEPALA Fokus posisi puluhan (digit ke-3) 40 poin
EKOR Fokus posisi satuan (digit ke-4) 40 poin

2. Machine Learning

Model Parameter Regularization
Random Forest n_estimators=50, max_depth=5, min_samples_split=10 ✅
Logistic Regression C=0.1, penalty='l2' ✅
Gradient Boosting n_estimators=50, max_depth=3, subsample=0.8 ✅

3. Feature Extraction (66 fitur)

· Frekuensi digit (10 fitur)
· Frekuensi per posisi (40 fitur)
· Trend moving average (1 fitur)
· Gap analysis (10 fitur)
· Pola 2D terakhir (2 fitur)
· Statistik (mean, std, min, max) (4 fitur)

---

🤖 MACHINE LEARNING

Mode ML

1. Mode Adaptif - Bobot otomatis menyesuaikan performa
2. Mode Manual - Bobot tetap sesuai pilihan user
3. Mode Off - Statistik only

Anti-Overfitting

· ✅ Cross Validation (TimeSeriesSplit)
· ✅ Max depth dibatasi
· ✅ Min samples split diperbesar
· ✅ Feature selection (max_features='sqrt')
· ✅ Ensemble of models
· ✅ Entropy-based certainty

Confidence & Certainty

· Confidence: Probabilitas tertinggi dari model
· Certainty: 1 - (entropy / max_entropy)
· Semakin tinggi certainty, semakin yakin model

---

📊 VALIDASI AKURASI

Menu validasi menampilkan:

· Mean Accuracy rata-rata
· Standard Deviation fluktuasi
· Last 10 Accuracy performa terkini
· Trend (naik/turun)
· Sample Predictions 5 prediksi terakhir

Contoh output:

```
📊 VALIDASI AKURASI METODE

6 ANGKA:
  Mean Accuracy : 42.35% 📈
  Std Deviation : 8.23%
  Last 10 Acc   : 48.57%
  Total Tests   : 98
  Sample Prediksi (5 terakhir):
    1. Pred: 3 7 1... | Aktual: 3715
    2. Pred: 5 2 8... | Aktual: 5284
```

---

📁 STRUKTUR FILE

```
📂 Project Folder
├── 📄 prediktor.py      # Aplikasi utama (menu, tampilan, interaksi user)
├── 📄 brainx.py         # Modul metode (statistik, ML, validasi, bobot adaptif)
├── 📄 README.md         # Dokumentasi
└── 📂 /sdcard/Download/ # Lokasi penyimpanan hasil prediksi
    ├── 📄 prediktor_adaptif_5_143022.txt
    ├── 📄 prediktor_manual_3_150245.txt
    └── 📄 prediktor_stat_7_161030.txt
```

File Output (.txt)

```
==================================================
  🔷 PREDIKTOR 6 ANGKA - HASIL LENGKAP
  🤖 ENSEMBLE ADAPTIF (ML:65% / STAT:35%)
==================================================
Pasaran: Singapore
Tanggal: 01/01/2024 14:30:22
Data: 156 putaran
Confidence ML: 73.45%
Certainty: 68.23%

🔷 6 ANGKA: 3*7*1*5*9*2
🏆 3D TOP : 7*3*9

🎯 7 KEPALA: 7*3*1*9*5*2*8
🎯 7 EKOR : 5*1*7*3*9*2*4

🔢 2D AUTO (78):
01*03*05*07*09*10*11*12*13*14...
```

---

🔧 TROUBLESHOOTING

1. Module not found

```bash
pip install requests numpy scikit-learn
```

2. SSL Error

```bash
pip install --upgrade certifi
```

3. Storage permission

```bash
termux-setup-storage
```

4. Data tidak muncul

· Cek koneksi internet
· Pastikan repository GitHub aktif
· Coba pasaran lain

5. ML tidak jalan

· Butuh minimal 40 data historis
· Cek apakah numpy & scikit-learn terinstall

6. Warna tidak muncul

```bash
# Termux biasanya sudah support ANSI color
# Jika tidak, install:
pkg install ncurses
```

---

📝 LISENSI

Prediktor 6 Angka dikembangkan oleh MOMODIGITAL untuk keperluan edukasi dan riset.

· ✅ Bebas digunakan untuk pembelajaran
· ✅ Boleh dimodifikasi
· ❌ Dilarang diperjualbelikan
· ❌ Tidak ada jaminan akurasi 100%

---

🙏 KREDIT & REFERENSI

· Data Source: MOMODIGITAL/data-vault
· Machine Learning: scikit-learn documentation
· Termux: termux.com
· Python: python.org

---

☕ SUPPORT

Jika aplikasi ini bermanfaat, Anda bisa:

· ⭐ Star repository di GitHub
· 🔄 Share ke teman-teman
· 🐛 Laporkan bug atau saran perbaikan

Selamat mencoba dan semoga beruntung! 🍀

---

```
==================================================
   🔷 PREDIKTOR 6 ANGKA - TERMUX EDITION
   🤖 DENGAN MACHINE LEARNING ADAPTIF
==================================================
```

```