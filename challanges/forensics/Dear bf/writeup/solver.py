import os
import zipfile

for i in range(64, 72):
    filename = f"photo{i}.png"
    if not os.path.exists(filename):
        print(f"[!] File {filename} not found, skipping...")
        continue
    with open(filename, "r+b") as f:
        header = f.read(8)
        if header == b'\x43\x4F\x4D\x50\x46\x45\x53\x54':
            f.seek(0)
            f.write(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')
            print(f"[+] Fixed PNG header for {filename}")
        else:
            print(f"[-] {filename} already fixed or unknown header")

for i in range(72, 81):
    filename = f"photo{i}.jpg"
    if not os.path.exists(filename):
        print(f"[!] File {filename} not found, skipping...")
        continue
    with open(filename, "r+b") as f:
        first_two = f.read(2)
        if first_two == b'\xFF\x17':
            f.seek(0)
            f.write(b'\xFF\xD8')
            print(f"[+] Fixed header for {filename}")
        else:
            print(f"[-] {filename} already fixed or wrong header")

secret_parts = []
for i in range(1, 64):
    zip_file = f"secret{i}.zip"
    with open(zip_file,"r+b") as f:
        f.seek(0)
        f.write(b'\x50')
        print(f"[+] Fixed header for {zip_file}")
    if not os.path.exists(zip_file):
        print(f"[!] {zip_file} not found, skipping unzip...")
        continue
    try:
        with zipfile.ZipFile(zip_file) as zf:
            extract_dir = f"unzipped_{i}"
            zf.extractall(extract_dir)
            print(f"[+] Unzipped {zip_file} to {extract_dir}")

            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    if file.startswith("secret") and file.endswith(".txt"):
                        part_path = os.path.join(root, file)
                        with open(part_path, "r", encoding="utf-8") as f:
                            content = f.read().strip()
                            secret_parts.append(content)
    except Exception as e:
        print(f"[!] Failed to unzip {zip_file}: {e}")

final_result = ''.join(secret_parts)
print(final_result)