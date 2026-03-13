from pwn import *

def main():
    context.log_level = "info"

    HOST = "localhost"
    PORT = 7000

    try:
        io = remote(HOST, PORT)
    except Exception as e:
        log.error(f"Gagal konek ke server: {e}")
        return

    answers = [
        # PART 1
        b"SAWIT67",
        b"SE Asia Standard Time",
        b"192.168.56.102",
        b"Windows 10 Home",
        b"6d6033b6b48902ee605fe5bba436f8dc",

        # PART 2
        b"2026-02-10 20:44:41",
        b"MicrosoftWordIntsaller.zip_192.168.56.1_8000",
        b"2026-02-10 23:34:58",
        b"2026-02-10 23:35:30",
        b"ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIvI7knMQfEaINUOcl/7YemBV3W8/obgj8ebIf6hmpH9 jaysen@LAPTOP-ULIU5NSO",
        b"T1098.004",

        # PART 3
        b"2026-02-10 23:55:17",
        b"whoami",
        b"scp",
        b"C:\\Windows\\Temp\\svch0st.exe",
        b"2026-02-10 16:56:29",
        b"J01nNe7sO5kar3NA_fAnSd3n9ant1psEn",
        b"197876"
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