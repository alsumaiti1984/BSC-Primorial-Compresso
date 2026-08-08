"""
============================================================
BSC v12.4 — Billion-Scale Direct Prime Predictor
============================================================
Author: BSC Lab 2026
Description:
    Computes huge primes (e.g., n = 100,000,000) directly
    without generating prior prime sequences.
============================================================
"""

import math
import numpy as np
import time

PRIMORIAL_2310 = 2310
COPRIME_2310 = set([r for r in range(PRIMORIAL_2310) if math.gcd(r, PRIMORIAL_2310) == 1])

def is_prime_miller_rabin(n):
    """فحص أولي حتمي ومطابق للمعايير القياسية"""
    if n < 2: return False
    if n in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37): return True
    if any(n % p == 0 for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)): return False
    
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
        
    # القواعد الحتمية المغطية لنطاقات حتى 2^64
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if n <= a: break
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True

def li_inverse_asymptotic_high_order(n):
    """توسعة مقاربة عالية الدقة من الرتبة الرابعة لمعكوس Li(n)"""
    log_n = math.log(n)
    log2_n = math.log(log_n)
    
    # Li⁻¹(n) ~ n * [ ln n + ln ln n - 1 + (ln ln n - 2)/ln n - (ln²ln n - 6 ln ln n + 11)/(2 ln² n) + ... ]
    term0 = log_n + log2_n - 1.0
    term1 = (log2_n - 2.0) / log_n
    term2 = -(log2_n**2 - 6.0 * log2_n + 11.0) / (2.0 * log_n**2)
    term3 = (log2_n**3 - 9.0 * log2_n**2 + 29.0 * log2_n - 32.0) / (3.0 * log_n**3)
    
    return n * (term0 + term1 + term2 + term3)

def predict_huge_prime(n):
    t0 = time.time()
    
    # 1. التنبؤ المقارب المباشر
    p_pred = li_inverse_asymptotic_high_order(n)
    
    # 2. توسيع نافذة البحث لتناسب النطاق الضخم O(sqrt(ln n))
    window_radius = int(2500 * (math.log(n) / math.log(100_000)))
    low_b = int(math.floor(p_pred - window_radius))
    high_b = int(math.ceil(p_pred + window_radius))
    
    # 3. الفلترة السريعة بموديول 2310
    candidates = [
        x for x in range(low_b, high_b + 1)
        if (x % PRIMORIAL_2310) in COPRIME_2310
    ]
    
    # 4. الترتيب بحسب القرب المباشر من المركز التنبؤي
    candidates.sort(key=lambda x: abs(x - p_pred))
    
    # 5. الفحص الحتمي
    checks = 0
    for cand in candidates:
        checks += 1
        if is_prime_miller_rabin(cand):
            elapsed = time.time() - t0
            return cand, p_pred, checks, elapsed
            
    return None, p_pred, checks, time.time() - t0

def run_billion_scale_test():
    print("=" * 70)
    print("BSC v12.4 BILLION-SCALE DIRECT PRIME GENERATOR TEST")
    print("=" * 70)
    
    # أهداف اختبارية في نطاقات ضخمة
    targets = [
        1_000_000,       # 1 مليون
        10_000_000,      # 10 ملايين
        50_000_000,      # 50 مليون
        100_000_000      # 100 مليون
    ]
    
    print(f"\n{'Target Index (n)':<18} | {'Predicted Prime':<20} | {'Checks':<8} | {'Time (s)':<10}")
    print("-" * 70)
    
    for n in targets:
        prime, pred, checks, t_sec = predict_huge_prime(n)
        print(f"{n:<18,} | {prime:<20,} | {checks:<8} | {t_sec:<10.4f}")
        
    print("=" * 70)

if __name__ == "__main__":
    run_billion_scale_test()