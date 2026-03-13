from pwn import *

def main():
    context.log_level = "info"

    HOST = "34.101.131.208"
    PORT = 8889

    try:
        io = remote(HOST, PORT)
    except Exception as e:
        log.error(f"Gagal konek ke server: {e}")
        return

    answers = [
        b"5.15.0-170",
        b"10.5.123.238_80_netsos",
        b"/home/tipsen/Downloads/netsos",
        b"a95640950eeaccdd09333ccad0c3db841fdb7c810bbde34c113279e63119dcb6",
        b"http://10.5.123.238:8080/api/v1/get_config",
        b"0634d24804cd0e5e9f6d543b95e7caedd9b118c3274723081a0983d09cd90307_th1s_1s_th3_IVVV",
        b"README.txt.enc,SuratEdaranLiburPuasa2026UniversitasIndonesia.pdf.enc,imej.jpg.enc,mydiary.pdf.enc",
        b"864758"
    ]

    for idx, ans in enumerate(answers, start=1):
        try:
            data = io.recvuntil(b"Answer:", timeout=5)

            print(f"\n=== Soal {idx} ===")
            print(data.decode(errors="ignore"))


            log.info(f"Sending: {ans.decode()}")
            io.sendline(ans)
        except EOFError:
            log.warning("Server memutus koneksi (EOF)")
            break

    io.interactive()

if __name__ == "__main__":
    main()
