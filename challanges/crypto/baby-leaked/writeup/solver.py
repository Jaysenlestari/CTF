from sage.all import *
from Crypto.Util.number import long_to_bytes, GCD as gcd
from pwn import remote
import time

def recover_p(N, p_known, total_bits=512, known_bits=416):
    F = PolynomialRing(Zmod(N), 'x') 
    x = F.gen()
    unknown_bits = total_bits - known_bits
    p_poly = p_known + (2 ** known_bits) * x
    f = p_poly.monic() 
    roots = f.small_roots(X=2 ** unknown_bits, beta=0.49)
    if roots:
        x0 = roots[0]
        p_recovered = p_known + (2 ** known_bits) * x0
        if N % int(p_recovered) == 0:
            return int(p_recovered)
    return None

def totient_coprime(totient, e):
    totient_coprime = totient
    while gcd(totient_coprime, e) != 1:
        totient_coprime //= gcd(totient_coprime, e)
    
    return totient_coprime

def find_roots(totient_coprime, e, n, rounds = 500):
    roots = set()
    roots.add(1)
    for i in range(2, rounds): 
        r = pow(i, totient_coprime, n)
        if pow(r, e, n) == 1:
            roots.add(r)
    
    return list(roots)

def decrypt(ct, d, n, roots, flag_prefix=b'NETSOS'):
    m = pow(ct, d, n)
    for i in roots:
        pt_bytes = long_to_bytes((m * i) % n)
        if flag_prefix in pt_bytes:
            return pt_bytes
        if pt_bytes.startswith(flag_prefix):
            return pt_bytes
            
    return None

def main():
    HOST = '127.0.0.1'
    PORT = 7103
    
    try:
        conn = remote(HOST, PORT)
    except Exception as e:
        print(f"Gagal terhubung ke {HOST}:{PORT} - {e}")
        return

    conn.sendlineafter(b'>> ', b'1')
    n_line = conn.recvline().strip()
    N = int(n_line.split(b': ')[1])
    print(f"Menerima N: {N}")

    conn.sendlineafter(b'>> ', b'2')
    leak_line = conn.recvline().strip()
    LSB = int(leak_line.split(b': ')[1])
    print(f"Menerima p_leak: {LSB}")

    print("\nMencoba recover p menggunakan Coppersmith...")
    p = recover_p(N, LSB)
    if p is None:
        print("Gagal recover p.")
        conn.close()
        return
    q = N // int(p)
    
    print(f"Sukses!")
    print(f"p = {p}")
    print(f"q = {q}")
    
    print("\nMengirim p dan q untuk mendapatkan flag terenkripsi...")
    conn.sendlineafter(b'>> ', b'3')
    conn.sendlineafter(b'Input p: ', str(p).encode())
    conn.sendlineafter(b'Input q: ', str(q).encode())
    
    ct_line = conn.recvline().strip()
    ct = int(ct_line.split(b': ')[1])
    print(f"Menerima Encrypted Flag (ct): {ct}")
    print("\nMendekripsi flag...")
    e = 16
    
    totient = (p - 1) * (q - 1)
    reduced_totient = int(totient_coprime(totient, e))
    d = pow(e, -1, reduced_totient)
    roots = find_roots(reduced_totient, e, N)
    pt = decrypt(ct, d, N, roots)
    
    if pt:
        print(f"\nFlag: {pt.decode('utf-8', 'ignore')}")
    else:
        print("\nGagal mendekripsi flag. Tidak menemukan prefix 'NETSOS'.")
    conn.close()

if __name__ == "__main__":
    main()