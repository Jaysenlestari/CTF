#!/usr/bin/env python3
import re, json, base64
from pathlib import Path
from collections import defaultdict

INPUT_FILE = Path("dump.json")
OUTPUT_FILE = Path("Lenovo_IdeaPad_Slim_5_16AKP10_Spec.pdf")

# Regex: tangkap variasi format part/chunk/data
PATTERNS = [
    re.compile(r'Part\s*(\d+)\s*/\s*(\d+)\s*(?:chunk\s*(\d+)\s*/\s*(\d+))?.*?data=([A-Za-z0-9+/=\s]+)'),
    re.compile(r'Part\s*(\d+)\s*written:.*?preview=([A-Za-z0-9+/=\s]+)'),
    re.compile(r'([A-Za-z0-9+/]{100,}={0,2})'),
]

def normalize_b64(s: str) -> str:
    return re.sub(r'\s+', '', s)

def find_base64_strings(txt: str):
    results = []
    for pat in PATTERNS[:2]:
        for m in pat.finditer(txt):
            if pat is PATTERNS[0]:
                part = int(m.group(1))
                chunk = int(m.group(3)) if m.group(3) else None
                b64 = normalize_b64(m.group(5))
            else:
                part = int(m.group(1))
                chunk = None
                b64 = normalize_b64(m.group(2))
            results.append((part, chunk, b64))
    # fallback long base64
    for m in PATTERNS[2].finditer(txt):
        results.append((None, None, normalize_b64(m.group(1))))
    return results

def extract_and_join():
    if not INPUT_FILE.exists():
        print(f"[!] File {INPUT_FILE} tidak ditemukan.")
        return

    raw = INPUT_FILE.read_text(encoding="utf-8", errors="ignore")

    b64_map = defaultdict(list)
    try:
        data = json.loads(raw)
        def walk(obj):
            if isinstance(obj, dict):
                for v in obj.values(): walk(v)
            elif isinstance(obj, list):
                for v in obj: walk(v)
            elif isinstance(obj, str):
                for part, chunk, b64 in find_base64_strings(obj):
                    if part is not None:
                        b64_map[part].append((chunk, b64))
        walk(data)
    except Exception:
        for part, chunk, b64 in find_base64_strings(raw):
            if part is not None:
                b64_map[part].append((chunk, b64))

    if not b64_map:
        print("[!] Tidak menemukan blok base64 dalam dump.json.")
        return

    combined = bytearray()
    for p in sorted(b64_map.keys()):
        chunks = sorted(b64_map[p], key=lambda x: (x[0] is None, x[0] or 1))
        joined = ''.join(c[1] for c in chunks)
        pad = len(joined) % 4
        if pad: joined += '=' * (4 - pad)
        try:
            decoded = base64.b64decode(joined, validate=False)
            combined.extend(decoded)
            print(f"[+] Part {p:02d} decoded ({len(decoded)} bytes)")
        except Exception as e:
            print(f"[!] Gagal decode part {p}: {e}")

    OUTPUT_FILE.write_bytes(combined)
    print(f"\n✅ Selesai! File disimpan sebagai '{OUTPUT_FILE}' ({len(combined)} bytes)")

if __name__ == "__main__":
    extract_and_join()