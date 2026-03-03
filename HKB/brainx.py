#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📦 MODUL METODE PREDIKSI - BRAINX
Versi Final dengan:
✅ Machine Learning (RF, LR, GB)
✅ Anti-Overfitting (Cross Validation, Regularization)
✅ Bobot Adaptif berdasarkan Performa
✅ ML untuk 8 Kepala dan 8 Ekor
✅ Ensemble ML + Statistik
✅ Feature Extraction 66 fitur
✅ 3D IRISAN 3 TAHAP (FILTER 2D + KEPALA*EKOR + 3D TOP)
"""

import numpy as np
from collections import Counter
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, TimeSeriesSplit
from sklearn.metrics import accuracy_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# ========== METODE STATISTIK ==========

def calc6(data):
    """
    Metode 6 ANGKA - Analisis frekuensi, posisi, dan pola 2D
    """
    if len(data) < 15:
        return {'h6': [], 'det': []}
    
    freq = Counter()
    pos = {i: Counter() for i in range(4)}
    d2_freq = Counter()
    
    for num in data:
        if len(num) != 4:
            continue
        for j in range(4):
            d = int(num[j])
            freq[d] += 1
            pos[j][d] += 1
        d2_freq[num[2:]] += 1
    
    scores = {}
    for digit in range(10):
        sc = 0
        max_f = max(freq.values()) or 1
        sc += (freq.get(digit, 0) / max_f) * 20
        f2 = sum(v for k, v in d2_freq.items() if str(digit) in k)
        max_2d = max(d2_freq.values()) or 1
        sc += (f2 / (max_2d * 2)) * 25
        ps = sum((pos[p].get(digit, 0) / (max(pos[p].values()) or 1)) * 7.5 for p in [2, 3])
        sc += ps
        scores[digit] = round(sc, 2)
    
    sorted_s = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return {'h6': [d for d, s in sorted_s[:6]], 'det': sorted_s}


def calc3(data):
    """
    Metode 3D TOP - Analisis dengan time decay dan gap
    """
    if len(data) < 15:
        return {'h3': [], 'det': []}
    
    n = len(data)
    freq = Counter()
    pos = {i: Counter() for i in [1, 2, 3]}
    gaps = {i: [] for i in range(10)}
    
    for idx, num in enumerate(data):
        if len(num) != 4:
            continue
        for p in [1, 2, 3]:
            d = int(num[p])
            freq[d] += 1
            pos[p][d] += 1
            gaps[d].append(idx)
    
    scores = {}
    for digit in range(10):
        sc = 0
        ts = sum((0.98 ** (n-1-j)) for j in range(n-1, -1, -1) if str(digit) in data[j][1:])
        sc += min(ts * 4, 25)
        weights = [5, 7, 8]
        for i, p in enumerate([1, 2, 3]):
            mx = max(pos[p].values()) or 1
            sc += (pos[p].get(digit, 0) / mx) * weights[i]
        gp = gaps[digit]
        if not gp:
            sc += 12
        else:
            lg = n - 1 - gp[-1]
            ag = n / (freq.get(digit, 1) or 1)
            if lg > ag*1.6:
                sc += 12
            elif lg > ag*1.2:
                sc += 8
            else:
                sc += 5
        sc += 4
        scores[digit] = round(sc, 2)
    
    sorted_s = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return {'h3': [d for d, s in sorted_s[:3]], 'det': sorted_s}


def calc_kepala(data):
    """
    Metode KEPALA - Fokus pada posisi puluhan
    MENJADI 8 ANGKA
    """
    if len(data) < 15:
        return []
    
    pos_freq = Counter()
    for num in data:
        if len(num) >= 3:
            d = int(num[2])
            pos_freq[d] += 1
    
    scores = {}
    for digit in range(10):
        sc = (pos_freq.get(digit, 0) / (max(pos_freq.values()) or 1)) * 40
        scores[digit] = round(sc, 2)
    
    sorted_s = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [d for d, s in sorted_s[:8]]  # 8 KEPALA


def calc_ekor(data):
    """
    Metode EKOR - Fokus pada posisi satuan
    MENJADI 8 ANGKA
    """
    if len(data) < 15:
        return []
    
    pos_freq = Counter()
    for num in data:
        if len(num) >= 4:
            d = int(num[3])
            pos_freq[d] += 1
    
    scores = {}
    for digit in range(10):
        sc = (pos_freq.get(digit, 0) / (max(pos_freq.values()) or 1)) * 40
        scores[digit] = round(sc, 2)
    
    sorted_s = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [d for d, s in sorted_s[:8]]  # 8 EKOR


def gen2d(top6):
    """
    Generate 2D dari top 6 angka
    """
    result = []
    for i in range(100):
        s = f"{i:02d}"
        if int(s[0]) in top6 or int(s[1]) in top6:
            result.append(s)
    return result


def gen3d(f2, top3):
    """
    Generate 3D combo dari 2D dan top 3
    """
    if not f2 or not top3:
        return []
    
    res, seen = [], set()
    for s in f2:
        a, b = int(s[0]), int(s[1])
        for x in top3:
            for p in [f"{a}{b}{x}", f"{a}{x}{b}", f"{b}{a}{x}", f"{b}{x}{a}", f"{x}{a}{b}", f"{x}{b}{a}"]:
                if p not in seen:
                    seen.add(p)
                    res.append(p)
    return sorted(res, key=int)


# ========== FUNGSI 3D IRISAN 3 TAHAP ==========

def gen_semua_3d_dari_top3(top3_digits):
    """
    TAHAP 2: Generate semua angka 000-999 yang mengandung setidaknya SATU digit dari top3
    Contoh: top3 = [6,1,4] → generate semua angka yang mengandung 6 atau 1 atau 4
    """
    if not top3_digits:
        return []
    
    # Konversi ke string untuk pengecekan
    top3_set = set(str(d) for d in top3_digits)
    hasil = []
    
    for i in range(1000):
        angka = f"{i:03d}"
        if any(d in top3_set for d in angka):
            hasil.append(angka)
    
    return hasil


def gen_3d_irisan_final(irisan_2d, top3_digits):
    """
    TAHAP 3: Generate 3D IRISAN FINAL berdasarkan:
    - irisan_2d: hasil irisan antara FILTER 2D dan KEPALA*EKOR (list 2D)
    - top3_digits: 3 digit top (misal: [6,1,4])
    
    Logika:
    - Generate semua angka 000-999 yang mengandung setidaknya SATU digit dari top3 (TAHAP 2)
    - Dari angka-angka tersebut, ambil yang 2 digit terakhirnya (2D belakang)
      ada di dalam irisan_2d (TAHAP 1)
    """
    if not irisan_2d or not top3_digits:
        return []
    
    # TAHAP 2: Generate semua 3D dari top3
    semua_3d = gen_semua_3d_dari_top3(top3_digits)
    
    # Konversi irisan_2d ke set untuk pengecekan cepat
    irisan_set = set(irisan_2d)
    
    # TAHAP 3: Filter berdasarkan 2D belakang
    hasil = []
    for angka in semua_3d:
        dua_d_belakang = angka[1:3]  # Ambil 2 digit terakhir
        if dua_d_belakang in irisan_set:
            hasil.append(angka)
    
    return hasil


# ========== VALIDASI AKURASI ==========

class ModelValidator:
    """
    Validasi akurasi prediksi dengan data historis
    """
    
    @staticmethod
    def backtest(data, metode_func, window_size=50, step=1):
        """
        Backtesting: Uji akurasi metode pada data historis
        """
        if len(data) < window_size + 10:
            return None
        
        predictions = []
        actuals = []
        accuracies = []
        
        for i in range(window_size, len(data)-1, step):
            train_data = data[i-window_size:i]
            test_actual = data[i]
            
            if metode_func.__name__ == 'calc6':
                pred_dict = metode_func(train_data)
                pred = pred_dict['h6']
            elif metode_func.__name__ == 'calc3':
                pred_dict = metode_func(train_data)
                pred = pred_dict['h3']
            else:
                pred = metode_func(train_data)
            
            predictions.append(pred)
            actuals.append(test_actual)
            
            if metode_func.__name__ == 'calc6':
                correct = sum(1 for d in pred if str(d) in test_actual)
                acc = correct / len(pred)
            elif metode_func.__name__ == 'calc3':
                correct = sum(1 for d in pred if str(d) in test_actual[1:])
                acc = correct / len(pred)
            else:
                if metode_func.__name__ == 'calc_kepala':
                    actual_digit = int(test_actual[2]) if len(test_actual) > 2 else -1
                elif metode_func.__name__ == 'calc_ekor':
                    actual_digit = int(test_actual[3]) if len(test_actual) > 3 else -1
                else:
                    actual_digit = -1
                
                if actual_digit != -1:
                    acc = 1.0 if actual_digit in pred else 0.0
                else:
                    acc = 0.0
            
            accuracies.append(acc)
        
        result = {
            'mean_accuracy': np.mean(accuracies) if accuracies else 0,
            'std_accuracy': np.std(accuracies) if accuracies else 0,
            'last_10_accuracy': np.mean(accuracies[-10:]) if len(accuracies) >= 10 else np.mean(accuracies) if accuracies else 0,
            'trend': np.polyfit(range(len(accuracies[-20:])), accuracies[-20:], 1)[0] if len(accuracies) >= 20 else 0,
            'total_tests': len(accuracies)
        }
        
        return result
    
    @staticmethod
    def compare_methods(data, methods):
        """Membandingkan akurasi berbagai metode"""
        results = {}
        for name, func in methods.items():
            result = ModelValidator.backtest(data, func)
            if result:
                results[name] = result
        return results


# ========== BOBOT ADAPTIF ==========

class AdaptiveWeightOptimizer:
    """
    Optimasi bobot berdasarkan performa historis
    """
    
    def __init__(self, learning_rate=0.1, decay=0.95):
        self.weights = {
            'statistik': 0.4,
            'ml_rf': 0.3,
            'ml_lr': 0.3
        }
        self.performance_history = []
        self.learning_rate = learning_rate
        self.decay = decay
        self.iteration = 0
        
    def update_weights(self, performances):
        """Update bobot berdasarkan performa terbaru"""
        self.iteration += 1
        self.performance_history.append(performances)
        
        if len(self.performance_history) > 10:
            total_weight = 0
            weighted_perf = {k: 0 for k in performances.keys()}
            
            for i, perf in enumerate(self.performance_history[-10:]):
                time_weight = self.decay ** (9 - i)
                total_weight += time_weight
                for k, v in perf.items():
                    weighted_perf[k] += v * time_weight
            
            for k in weighted_perf:
                weighted_perf[k] /= total_weight
        else:
            weighted_perf = performances
        
        total_perf = sum(weighted_perf.values())
        if total_perf > 0:
            new_weights = {}
            for k, v in weighted_perf.items():
                target_weight = v / total_perf
                new_weights[k] = self.weights.get(k, 0) * (1 - self.learning_rate) + \
                                 target_weight * self.learning_rate
            
            total = sum(new_weights.values())
            for k in new_weights:
                new_weights[k] /= total
            
            self.weights = new_weights
        
        return self.weights
    
    def get_weights(self):
        return self.weights
    
    def get_ml_weight(self):
        return self.weights.get('ml_rf', 0) + self.weights.get('ml_lr', 0)
    
    def get_stat_weight(self):
        return self.weights.get('statistik', 0.4)


# ========== MACHINE LEARNING DENGAN ANTI-OVERFITTING ==========

class RobustMLPredictor:
    """
    ML Predictor dengan teknik anti-overfitting
    """
    
    def __init__(self):
        self.models = []
        self.scaler = StandardScaler()
        self.accuracies = []
        self.is_trained = False
        self.confidence = 0
        self.cv_scores = []
        
    def extract_features(self, data, index):
        """Ekstrak 66 fitur dari data historis"""
        features = []
        window = min(20, index)
        
        if index < 10:
            return None
        
        start_idx = max(0, index - window)
        window_data = data[start_idx:index]
        
        # 1. Frekuensi setiap digit (10 fitur)
        digit_freq = [0] * 10
        for num in window_data:
            if len(num) == 4:
                for d in num:
                    digit_freq[int(d)] += 1
        total_digits = len(window_data) * 4
        if total_digits > 0:
            digit_freq = [f/total_digits for f in digit_freq]
        features.extend(digit_freq)
        
        # 2. Frekuensi per posisi (40 fitur)
        for pos in range(4):
            pos_counts = [0] * 10
            for num in window_data:
                if len(num) == 4:
                    d = int(num[pos])
                    pos_counts[d] += 1
            if len(window_data) > 0:
                pos_counts = [c/len(window_data) for c in pos_counts]
            features.extend(pos_counts)
        
        # 3. Trend (1 fitur)
        if index >= 5:
            recent_nums = data[index-5:index]
            recent_avg = sum(int(n) for n in recent_nums if len(n)==4) / (len(recent_nums)*4)
            older_avg = sum(int(n) for n in data[index-10:index-5] if len(n)==4) / 20
            features.append(recent_avg - older_avg)
        else:
            features.append(0)
        
        # 4. Gap analysis (10 fitur)
        gaps = []
        for digit in range(10):
            last_pos = -1
            for i, num in enumerate(data[:index]):
                if len(num) == 4 and str(digit) in num:
                    last_pos = i
            if last_pos == -1:
                gaps.append(index)
            else:
                gaps.append(index - last_pos - 1)
        max_gap = max(gaps) if max(gaps) > 0 else 1
        gaps = [g/max_gap for g in gaps]
        features.extend(gaps)
        
        # 5. Pola 2D terakhir (2 fitur)
        if len(window_data) >= 2:
            last_2d = [num[2:] for num in window_data[-2:] if len(num)==4]
            features.extend([int(last_2d[0])/100 if last_2d else 0, 
                           int(last_2d[-1])/100 if len(last_2d)>1 else 0])
        else:
            features.extend([0, 0])
        
        # 6. Statistik (4 fitur)
        if window_data:
            nums_int = [int(n) for n in window_data if len(n)==4]
            if nums_int:
                features.append(np.mean(nums_int)/10000)
                features.append(np.std(nums_int)/10000)
                features.append(min(nums_int)/10000)
                features.append(max(nums_int)/10000)
            else:
                features.extend([0, 0, 0, 0])
        else:
            features.extend([0, 0, 0, 0])
        
        return features
    
    def train_with_cv(self, data):
        """Training dengan Cross Validation untuk mencegah overfitting"""
        if len(data) < 40:
            return False
        
        X = []
        y_digits = [[] for _ in range(4)]
        
        for i in range(20, len(data)-1):
            features = self.extract_features(data, i)
            if features:
                X.append(features)
                next_num = data[i+1]
                if len(next_num) == 4:
                    for pos in range(4):
                        y_digits[pos].append(int(next_num[pos]))
        
        if len(X) < 20:
            return False
        
        X = np.array(X)
        X_scaled = self.scaler.fit_transform(X)
        
        tscv = TimeSeriesSplit(n_splits=5)
        
        self.models = []
        self.accuracies = []
        self.cv_scores = []
        
        for pos in range(4):
            y = np.array(y_digits[pos])
            pos_models = []
            pos_scores = []
            
            # Model 1: Random Forest
            rf_model = RandomForestClassifier(
                n_estimators=50, max_depth=5, 
                min_samples_split=10, min_samples_leaf=5,
                max_features='sqrt', random_state=42, n_jobs=-1
            )
            cv_scores_rf = cross_val_score(rf_model, X_scaled, y, cv=tscv, scoring='accuracy')
            mean_cv_rf = np.mean(cv_scores_rf)
            rf_model.fit(X_scaled, y)
            pos_models.append(('rf', rf_model))
            pos_scores.append(mean_cv_rf)
            
            # Model 2: Logistic Regression
            lr_model = LogisticRegression(
                C=0.1, max_iter=1000, random_state=42,
                multi_class='ovr', penalty='l2', solver='lbfgs'
            )
            cv_scores_lr = cross_val_score(lr_model, X_scaled, y, cv=tscv, scoring='accuracy')
            mean_cv_lr = np.mean(cv_scores_lr)
            lr_model.fit(X_scaled, y)
            pos_models.append(('lr', lr_model))
            pos_scores.append(mean_cv_lr)
            
            # Model 3: Gradient Boosting
            gb_model = GradientBoostingClassifier(
                n_estimators=50, max_depth=3, learning_rate=0.1,
                subsample=0.8, random_state=42
            )
            cv_scores_gb = cross_val_score(gb_model, X_scaled, y, cv=tscv, scoring='accuracy')
            mean_cv_gb = np.mean(cv_scores_gb)
            gb_model.fit(X_scaled, y)
            pos_models.append(('gb', gb_model))
            pos_scores.append(mean_cv_gb)
            
            best_idx = np.argmax(pos_scores)
            best_model = pos_models[best_idx][1]
            best_score = pos_scores[best_idx]
            
            self.models.append(best_model)
            self.accuracies.append(best_score)
            self.cv_scores.append({
                'rf': mean_cv_rf,
                'lr': mean_cv_lr,
                'gb': mean_cv_gb,
                'best': pos_models[best_idx][0]
            })
        
        self.is_trained = True
        return True
    
    def predict_with_ensemble(self, data):
        """Prediksi dengan ensemble dan confidence score"""
        if not self.is_trained:
            return None
        
        latest_features = self.extract_features(data, len(data)-1)
        if not latest_features:
            return None
        
        X_latest = self.scaler.transform([latest_features])
        
        predictions = []
        probabilities = []
        top_digits = {i: [] for i in range(4)}
        all_probs = []
        
        for i, model in enumerate(self.models):
            pred = model.predict(X_latest)[0]
            predictions.append(pred)
            
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(X_latest)[0]
                proba = np.clip(proba, 0.01, 0.99)
                proba = proba / proba.sum()
                prob = max(proba)
                probabilities.append(prob)
                all_probs.append(proba)
                
                digit_probs = [(j, proba[j]) for j in range(len(proba))]
                digit_probs.sort(key=lambda x: x[1], reverse=True)
                top_digits[i] = [d for d, p in digit_probs[:7]]
            else:
                probabilities.append(0.5)
                all_probs.append(np.array([0.1]*10))
        
        if all_probs:
            ensemble_proba = np.mean(all_probs, axis=0)
            self.confidence = np.max(ensemble_proba)
            
            mean_proba = np.mean(all_probs, axis=0)
            entropy = -np.sum(mean_proba * np.log(mean_proba + 1e-10))
            max_entropy = -np.log(1/10)
            certainty = 1 - (entropy / max_entropy)
        else:
            self.confidence = 0.5
            certainty = 0.5
        
        return {
            'predictions': predictions,
            'probabilities': probabilities,
            'confidence': self.confidence,
            'certainty': certainty,
            'top_digits': top_digits,
            'accuracies': self.accuracies,
            'cv_scores': self.cv_scores
        }
    
    def predict_kepala_ekor(self, data):
        """
        Prediksi khusus untuk KEPALA (posisi 3) dan EKOR (posisi 4)
        MENJADI 8 ANGKA
        """
        if not self.is_trained or len(self.models) < 4:
            return None, None
        
        latest_features = self.extract_features(data, len(data)-1)
        if not latest_features:
            return None, None
        
        X_latest = self.scaler.transform([latest_features])
        
        # Model untuk KEPALA (index 2 = posisi puluhan)
        if len(self.models) > 2:
            model_kepala = self.models[2]
            if hasattr(model_kepala, 'predict_proba'):
                proba_kepala = model_kepala.predict_proba(X_latest)[0]
                kepala_probs = [(j, proba_kepala[j]) for j in range(len(proba_kepala))]
                kepala_probs.sort(key=lambda x: x[1], reverse=True)
                kepala_ml = [d for d, p in kepala_probs[:8]]  # 8 KEPALA
            else:
                kepala_ml = []
        else:
            kepala_ml = []
        
        # Model untuk EKOR (index 3 = posisi satuan)
        if len(self.models) > 3:
            model_ekor = self.models[3]
            if hasattr(model_ekor, 'predict_proba'):
                proba_ekor = model_ekor.predict_proba(X_latest)[0]
                ekor_probs = [(j, proba_ekor[j]) for j in range(len(proba_ekor))]
                ekor_probs.sort(key=lambda x: x[1], reverse=True)
                ekor_ml = [d for d, p in ekor_probs[:8]]  # 8 EKOR
            else:
                ekor_ml = []
        else:
            ekor_ml = []
        
        return kepala_ml, ekor_ml


# ========== ENSEMBLE DENGAN BOBOT ADAPTIF ==========

def ensemble_prediction_adaptive(data, ml_result, h6_stat, h3_stat, optimizer=None):
    """
    Ensemble dengan bobot adaptif berdasarkan performa
    """
    if not ml_result:
        return h6_stat, h3_stat, None
    
    if optimizer is None:
        optimizer = AdaptiveWeightOptimizer()
    
    weights = optimizer.get_weights()
    ml_weight = weights.get('ml_rf', 0.3) + weights.get('ml_lr', 0.3)
    stat_weight = weights.get('statistik', 0.4)
    
    # Ensemble untuk 6 ANGKA
    combined_scores = {}
    
    for pos, top_digits in ml_result['top_digits'].items():
        for rank, digit in enumerate(top_digits[:6]):
            score = (6 - rank) * ml_weight * ml_result['certainty']
            combined_scores[digit] = combined_scores.get(digit, 0) + score
    
    for rank, digit in enumerate(h6_stat['h6']):
        score = (6 - rank) * stat_weight
        combined_scores[digit] = combined_scores.get(digit, 0) + score
    
    sorted_digits = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    ensemble_h6 = [d for d, s in sorted_digits[:6]]
    
    # Ensemble untuk 3D
    ml_top3 = []
    for pos in [1, 2, 3]:
        if pos in ml_result['top_digits'] and ml_result['top_digits'][pos]:
            ml_top3.append(ml_result['top_digits'][pos][0])
    
    all_candidates = list(set(ml_top3 + h3_stat['h3']))
    h3_scores = {}
    
    for digit in all_candidates:
        score = 0
        if digit in ml_top3:
            score += ml_weight * ml_result['certainty']
        if digit in h3_stat['h3']:
            score += stat_weight
        h3_scores[digit] = score
    
    sorted_h3 = sorted(h3_scores.items(), key=lambda x: x[1], reverse=True)
    ensemble_h3 = [d for d, s in sorted_h3[:3]]
    
    return {'h6': ensemble_h6, 'det': []}, {'h3': ensemble_h3, 'det': []}, optimizer


# ========== FUNGSI UTAMA YANG DIPANGGIL ==========

def hitung_semua(data, use_ml=True, ml_weight=0.6, optimizer=None, verbose=False, 
                 filter_2d_list=None, irisan_2d=None):
    """
    Fungsi utama yang memanggil semua metode dengan fitur lengkap
    filter_2d_list: hasil filter 2D dari user (opsional)
    irisan_2d: hasil irisan antara FILTER 2D dan KEPALA*EKOR (opsional, untuk 3D final)
    """
    hasil = {
        'statistik': {},
        'ml': None,
        'ensemble': None,
        'validasi': None,
        'optimizer': optimizer,
        'final': {}
    }
    
    # 1. Metode statistik
    hasil['statistik'] = {
        'h6': calc6(data),
        'h3': calc3(data),
        'kepala': calc_kepala(data),
        'ekor': calc_ekor(data)
    }
    
    # 2. Machine Learning
    if use_ml and len(data) >= 40:
        ml_predictor = RobustMLPredictor()
        if ml_predictor.train_with_cv(data):
            ml_result = ml_predictor.predict_with_ensemble(data)
            
            # Dapatkan prediksi khusus untuk Kepala dan Ekor
            kepala_ml, ekor_ml = ml_predictor.predict_kepala_ekor(data)
            
            hasil['ml'] = {
                'result': ml_result,
                'predictor': ml_predictor,
                'kepala_ml': kepala_ml,
                'ekor_ml': ekor_ml
            }
            
            # 3. Ensemble dengan bobot adaptif
            if optimizer is None:
                optimizer = AdaptiveWeightOptimizer()
            
            h6_ensemble, h3_ensemble, optimizer = ensemble_prediction_adaptive(
                data, ml_result, 
                hasil['statistik']['h6'], 
                hasil['statistik']['h3'],
                optimizer
            )
            
            # Ensemble untuk Kepala dan Ekor
            kepala_stat = hasil['statistik']['kepala']
            ekor_stat = hasil['statistik']['ekor']
            
            ml_weight_final = optimizer.get_ml_weight()
            stat_weight_final = 1 - ml_weight_final
            
            # Ensemble Kepala (menjadi 8)
            if kepala_ml:
                kepala_combined = {}
                for d in set(kepala_ml[:6] + kepala_stat[:6]):
                    score = 0
                    if d in kepala_ml[:6]:
                        score += ml_weight_final * ml_result['certainty']
                    if d in kepala_stat[:6]:
                        score += stat_weight_final
                    kepala_combined[d] = score
                
                sorted_kepala = sorted(kepala_combined.items(), key=lambda x: x[1], reverse=True)
                kepala_final = [d for d, s in sorted_kepala[:8]]
            else:
                kepala_final = kepala_stat[:8]
            
            # Ensemble Ekor (menjadi 8)
            if ekor_ml:
                ekor_combined = {}
                for d in set(ekor_ml[:6] + ekor_stat[:6]):
                    score = 0
                    if d in ekor_ml[:6]:
                        score += ml_weight_final * ml_result['certainty']
                    if d in ekor_stat[:6]:
                        score += stat_weight_final
                    ekor_combined[d] = score
                
                sorted_ekor = sorted(ekor_combined.items(), key=lambda x: x[1], reverse=True)
                ekor_final = [d for d, s in sorted_ekor[:8]]
            else:
                ekor_final = ekor_stat[:8]
            
            hasil['ensemble'] = {
                'h6': h6_ensemble,
                'h3': h3_ensemble,
                'ml_weight': optimizer.get_ml_weight(),
                'stat_weight': optimizer.get_stat_weight(),
                'confidence': ml_result['confidence'],
                'certainty': ml_result['certainty'],
                'weights': optimizer.get_weights(),
                'kepala_ml': kepala_ml,
                'ekor_ml': ekor_ml
            }
            hasil['optimizer'] = optimizer
            
            # Update final dengan hasil ensemble Kepala/Ekor
            hasil['final']['kepala'] = kepala_final
            hasil['final']['ekor'] = ekor_final
            hasil['final']['metode'] = 'ensemble'
        else:
            # ML gagal training
            hasil['final']['kepala'] = hasil['statistik']['kepala'][:8]
            hasil['final']['ekor'] = hasil['statistik']['ekor'][:8]
            hasil['final']['metode'] = 'statistik'
    else:
        # ML tidak digunakan
        hasil['final']['kepala'] = hasil['statistik']['kepala'][:8]
        hasil['final']['ekor'] = hasil['statistik']['ekor'][:8]
        hasil['final']['metode'] = 'statistik'
    
    # Tentukan final untuk 6 ANGKA dan 3D
    if hasil['ensemble']:
        hasil['final']['h6'] = hasil['ensemble']['h6']['h6']
        hasil['final']['h3'] = hasil['ensemble']['h3']['h3']
    else:
        hasil['final']['h6'] = hasil['statistik']['h6']['h6']
        hasil['final']['h3'] = hasil['statistik']['h3']['h3']
    
    # Generate kombinasi standar
    hasil['final']['c2'] = gen2d(hasil['final']['h6'])
    hasil['final']['c3'] = gen3d(hasil['final']['c2'], hasil['final']['h3'])
    
    # Generate Kepala*Ekor
    ke_combo = []
    for k in hasil['final']['kepala']:
        for e in hasil['final']['ekor']:
            ke_combo.append(f"{k}{e}")
    hasil['final']['ke_combo'] = ke_combo
    
    # Generate 3D IRISAN FINAL (3 TAHAP) jika irisan_2d diberikan
    if irisan_2d and len(irisan_2d) > 0:
        hasil['final']['c3_irisan_final'] = gen_3d_irisan_final(
            irisan_2d,
            hasil['final']['h3']  # top3 digits
        )
    else:
        hasil['final']['c3_irisan_final'] = []
    
    return hasil


# Untuk testing
if __name__ == "__main__":
    print("="*60)
    print("📦 BRAINX MODULE - VERSI FINAL")
    print("✅ Metode Statistik")
    print("✅ Machine Learning (RF, LR, GB)")
    print("✅ Anti-Overfitting")
    print("✅ Bobot Adaptif")
    print("✅ 8 KEPALA & 8 EKOR")
    print("✅ 3D IRISAN 3 TAHAP (FILTER 2D + KEPALA*EKOR + 3D TOP)")
    print("="*60)
