# Writeup <baby-leaked>

Challenge ini adalah masalah kripto RSA dengan dua bagian utama. Pertama, kita diberi leak bit dari $p$, dan kedua, kita diberi eksponen publik $e=16$ yang tidak coprime dengan $\phi(n)$.

## Bagian 1  
Kita diberikan $N$ (1024 bit) dan $p_{\text{leak}}$, yaitu 416 bit LSB (bit-bit akhir) dari p. Karena p adalah 512 bit, kita kehilangan $512 - 416 = 96$ bit (bit-bit awal/MSB).Kita dapat memodelkan p sebagai polinomial dalam satu variabel $x$, di mana $x$ adalah 96 bit yang tidak diketahui:

$p(x) = (x \cdot 2^{416}) + p_{\text{leak}}$

Karena $p$ adalah faktor dari $N$, kita dapat menemukan $x$ dengan mencari akar kecil dari $f(x) = p(x) ≡ 0 (mod N)$. Kita dapat menggunakan coppersmith's small root attack untuk merekontruksi $p$ nya.

## Bagian 2: 
Permasalahan kedua adalah $e=16$. Kita tidak bisa menghitung $d$ secara langsung karena $\gcd(E, \phi(N)) \neq 1$. Solusinya adalah menggunakan "Reduced Totient" ($\lambda'$) dan mencari "Roots of Unity". Hitung 

1. $\phi(N)$:$\phi = (p - 1) \cdot (q - 1)$ 
2. Hitung "Reduced Totient" ($\lambda'$): Kita butuh $\lambda'$ yang coprime dengan $E$. Kita lakukan ini dengan membagi semua faktor 2 dari $\phi$ hingga gcd(e, λ') = 1.
3. Hitung private key $d$:
Sekarang kita bisa menghitung $d$ menggunakan $\lambda'$. $\,\,d = E^{-1} \pmod{\lambda'}$
4. Selanjutnya tinggal melakukan decryption seperti biasa $m'\,=\,c^d \,mod\,n$. Namun hasil ini belum tentu merupakan plaintext yang benar. Plaintext yang valid adalah $m = (m' * r) mod N$ di mana $r$ merupakan salah satu dari $gcd(e, φ(N)) = 16$.