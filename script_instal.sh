#!/bin/bash
# Script lengkap: Download + Install Dependencies + Jalankan

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}================================================${NC}"
echo -e "${GREEN}  🔷 PREDIKTOR 6 ANGKA - INSTALLER TERMUX${NC}"
echo -e "${CYAN}================================================${NC}"
echo ""

# 1. Update pkg
echo -e "${YELLOW}📦 Update package list...${NC}"
pkg update -y && pkg upgrade -y

# 2. Install Python
echo -e "\n${YELLOW}🐍 Install Python...${NC}"
pkg install python -y

# 3. Install pip
echo -e "\n${YELLOW}📦 Install pip...${NC}"
pkg install python-pip -y

# 4. Download files
echo -e "\n${YELLOW}📥 Download script dari GitHub...${NC}"
curl -s -o brainx.py https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/brainx.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ brainx.py${NC}"
else
    echo -e "${RED}   ❌ brainx.py${NC}"
fi

curl -s -o prediktor.py https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/prediktor.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ prediktor.py${NC}"
else
    echo -e "${RED}   ❌ prediktor.py${NC}"
fi

# 5. Install Python dependencies
echo -e "\n${YELLOW}📦 Install Python modules...${NC}"
pip install requests numpy scikit-learn

# 6. Cek hasil
echo -e "\n${CYAN}================================================${NC}"
if [ -f "brainx.py" ] && [ -f "prediktor.py" ]; then
    echo -e "${GREEN}✅ INSTALASI SELESAI!${NC}"
    echo -e ""
    echo -e "${YELLOW}📂 File yang tersedia:${NC}"
    ls -la brainx.py prediktor.py
    
    echo -e ""
    echo -e "${CYAN}🚀 Jalankan program:${NC}"
    echo -e "   ${GREEN}python prediktor.py${NC}"
    
    echo -e ""
    echo -e "${YELLOW}📊 Menu yang tersedia:${NC}"
    echo -e "   1. Prediksi Pasaran"
    echo -e "   2. Konfigurasi ML Adaptif"
    echo -e "   3. Validasi Akurasi"
    echo -e "   4. Keluar"
    
    # Tanya apakah mau langsung menjalankan
    echo -e ""
    read -p "$(echo -e ${CYAN}🔥 Jalankan sekarang? (y/n): ${NC})" run_now
    if [ "$run_now" = "y" ] || [ "$run_now" = "Y" ]; then
        echo -e "\n${GREEN}Menjalankan prediktor.py...${NC}\n"
        python prediktor.py
    fi
else
    echo -e "${RED}❌ GAGAL: File tidak lengkap${NC}"
    echo -e "${YELLOW}Coba download manual:${NC}"
    echo "   curl -o brainx.py https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/brainx.py"
    echo "   curl -o prediktor.py https://raw.githubusercontent.com/momodigital/brainx/refs/heads/main/HKB/prediktor.py"
fi
echo -e "${CYAN}================================================${NC}"
