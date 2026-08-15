import numpy as np
from sympy import primerange, prime, nextprime, prevprime, primepi

# cache لأول 10,000 عدد أولي للسرعة
PRIMES_CACHE = list(primerange(1, 105000))

def BSC_v17_2_optimized(n: int) -> int:
    n = int(n)
    
    # 1. الاسترجاع السريع من الـ Cache
    if n <= len(PRIMES_CACHE):
        return PRIMES_CACHE[n - 1]

    # 2. تقريب Cipolla كبداية ممتازة
    L1 = np.log(n)
    L2 = np.log(L1)
    p_approx = n * (L1 + L2 - 1.0 + (L2 - 2.0)/L1 - (L2**2 - 6*L2 + 17.0)/(2.0*L1**2))
    p = int(round(p_approx))
    
    # 3. الضبط الدقيق مع التقليل من استدعاء primepi
    current_pi = primepi(p)
    
    while current_pi < n:
        p = nextprime(p)
        current_pi += 1
        
    while current_pi > n:
        p = prevprime(p)
        current_pi -= 1
        
    return p

# استقبال الإدخال من المستخدم
if __name__ == "__main__":
    try:
        user_input = input("أدخل رتبة العدد الأولي المطلوب (n): ")
        n = int(user_input)
        
        if n <= 0:
            print("عذراً، يجب أن تكون الرتبة عداً صحيحاً موجباً أكبر من 0.")
        else:
            result = BSC_v17_2_optimized(n)
            print(f"العدد الأولي رقم {n} هو: {result}")
            
    except ValueError:
        print("خطأ: يرجى إدخال عدد صحيح فقط.")