def reverse_joined(joined: str):
    # pecah tiap 3 digit
    triplets = [joined[i:i+3] for i in range(0, len(joined), 3)]

    # convert 3-digit decimal → int
    nums = [int(t) for t in triplets]

    # convert int → hex
    hex_bytes = [format(n, '02x') for n in nums]

    # convert int → ASCII char
    ascii_str = ''.join(chr(n) for n in nums)

    return hex_bytes, ascii_str


# === Example usage ===
joined = "080065082084032050032058032084049110103103097108095051107115116114065107095116051082085115095105110102111045105110102111013010"

hex_out, ascii_out = reverse_joined(joined)

print("HEX :", " ".join(hex_out))
print("ASCII:", ascii_out)
