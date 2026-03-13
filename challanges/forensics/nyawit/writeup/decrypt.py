import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

KEY = b'J01nNe7sO5kar3NA'
IV  = b'fAnSd3n9ant1psEn'

def decrypt_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            ciphertext = f.read()

        cipher = AES.new(KEY, AES.MODE_CBC, IV)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        new_path = file_path + ".decrypted"

        with open(new_path, 'wb') as f:
            f.write(plaintext)

        print(f"[+] SUCCESS Decrypted: {file_path} -> {new_path}")

    except Exception as e:
        print(f"[-] FAILED on {file_path}: {e}")

if __name__ == "__main__":
    target_dir = "."
    print("[*] Scanning current directory for .enc files...")

    for file in os.listdir(target_dir):
        if file.endswith('.enc'):
            decrypt_file(file)

    print("[*] Decryption process finished!")