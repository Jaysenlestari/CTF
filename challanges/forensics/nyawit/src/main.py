def main():
    print("\n⚠️  Multi-part Digital Forensic Investigation Challenge ⚠️")
    print("Solve each part to uncover the full attack chain.\n")

    answers = [
        # PART 1
        "SAWIT67",
        "SE Asia Standard Time",
        "192.168.56.102",
        "Windows 10 Home",
        "6d6033b6b48902ee605fe5bba436f8dc",

        # PART 2
        "2026-02-10 20:44:41",
        "MicrosoftWordIntsaller.zip_192.168.56.1_8000",
        "2026-02-10 23:34:58",
        "2026-02-10 23:35:30",
        "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIvI7knMQfEaINUOcl/7YemBV3W8/obgj8ebIf6hmpH9 jaysen@LAPTOP-ULIU5NSO", 
        "T1098.004",

        # PART 3
        "2026-02-10 23:55:17",
        "whoami",
        "scp",
        "C:\\Windows\Temp\svch0st.exe",
        "2026-02-10 16:56:29",
        "J01nNe7sO5kar3NA_fAnSd3n9ant1psEn",
        "197876"
    ]

    questions = [
        # ================= PART 1 =================
        ("PART 1 — REGISTRY, SYSTEM & USER ARTIFACTS",
         "What is the computer name (hostname) of the compromised system?",
         "Hostname (e.g., DESKTOP-1234ABC)"),

        ("PART 1 — REGISTRY, SYSTEM & USER ARTIFACTS",
         "What is the configured time zone of the system?",
         "Time Zone String (e.g., Pacific Standard Time)"),

        ("PART 1 — REGISTRY, SYSTEM & USER ARTIFACTS",
         "What is the dynamically assigned IPv4 address of the system?",
         "IPv4 address (e.g., 192.168.12.50)"),

        ("PART 1 — REGISTRY, SYSTEM & USER ARTIFACTS",
         "Identify the exact operating system installed on the machine.",
         "OS Edition (e.g., Windows 11 IoT Enterprise)"),

        ("PART 1 — REGISTRY, SYSTEM & USER ARTIFACTS",
         "What is the NTLM hash of the non-system user account that has a password configured?",
         "NTLM Hash (32 hex characters)"),

        # ================= PART 2 =================
        ("PART 2 — PERSISTENCE & INITIAL COMPROMISE",
         "When did the victim first visit http://jaysenlestari.github.io/ ? (system local time)",
         "YYYY-MM-DD HH:MM:SS"),

        ("PART 2 — PERSISTENCE & INITIAL COMPROMISE",
         "What is the name of the malicious file that the victim believed to be a software installer, and what are the IP address and port of the server from which it was downloaded?",
         "<filename>_<ip_address>_<port>"),

        ("PART 2 — PERSISTENCE & INITIAL COMPROMISE",
         "When did the victim finish extracting the downloaded installer? (System local time)",
         "YYYY-MM-DD HH:MM:SS"),

        ("PART 2 — PERSISTENCE & INITIAL COMPROMISE",
        "When did the victim execute the malicious script for the first time? (System local time)",
         "YYYY-MM-DD HH:MM:SS"),

        ("PART 2 — PERSISTENCE & INITIAL COMPROMISE",
         "What SSH public key was added to the victim's authorized_keys file?",
         "ssh-ed25519 <base64_key> user@host"),

        ("PART 2 — PERSISTENCE & INITIAL COMPROMISE",
         "Based on this finding, what is the corresponding MITRE ATT&CK technique ID for this persistence behavior?",
         "TXXXX.XXX"),

        # ================= PART 3 =================
        ("PART 3 — REMOTE ACCESS & POST-EXPLOITATION",
         "At what exact time did the attacker successfully establish an interactive shell connection via SSH? (System local time)",
         "YYYY-MM-DD HH:MM:SS"),

        ("PART 3 — REMOTE ACCESS & POST-EXPLOITATION",
         "After gaining initial access, what was the first command executed by the attacker?",
         "command (e.g., ipconfig)"),

        ("PART 3 — REMOTE ACCESS & POST-EXPLOITATION",
         "What command-line tool did the attacker use to transfer the malicious binary to the victim system?",
         "tool name (e.g., wget, curl)"),

        ("PART 3 — REMOTE ACCESS & POST-EXPLOITATION",
         "Where was the malicious binary located on the victim system?",
         "DriveLetter:\\Path\\Filename.exe"),

        ("PART 3 — REMOTE ACCESS & POST-EXPLOITATION",
         "When did the attacker execute the malicious binary from their shell? (System local time)",
         "YYYY-MM-DD HH:MM:SS"),

        ("PART 3 — REMOTE ACCESS & POST-EXPLOITATION",
         "What are the encryption key and initialization vector (IV) embedded within the malicious binary?",
         "<key>_<iv>"),

        ("PART 3 — REMOTE ACCESS & POST-EXPLOITATION",
         "What bank PIN did the victim hide inside the encrypted file?",
         "<number>")
    ]

    current_part = ""
    correct_count = 0

    for i, (part, question, fmt) in enumerate(questions):
        if part != current_part:
            current_part = part
            print("\n" + "=" * 80)
            print(current_part)
            print("=" * 80)

        print("\n" + "-" * 80)
        print(f"Question {i+1}/{len(questions)}")
        print(question)
        print(f"Format: {fmt}")
        print("-" * 80)

        user_answer = input("Answer: ").strip()
        expected_answer = answers[i]

        is_correct = user_answer.strip().lower() == str(expected_answer).strip().lower()
        if is_correct:
            correct_count += 1
            print("Correct!")
        else:
            print("Incorrect! Investigation terminated.")
            return
        
        if i == 4:
            print("\n🧩 Part 1 Complete.")
            print("You now have a solid starting point for the investigation.")
        elif i == 10:
            print("\n🔐 Part 2 Complete.")
            print("You have uncovered how the attacker maintained access.")
        elif i == 17:
            print("\n🕵️ Part 3 Complete.")
            print("You have reconstructed the attacker’s actions.")

    if correct_count == len(questions):
        print("\n" + "=" * 80)
        print("🎉 INVESTIGATION COMPLETE 🎉")
        print("=" * 80)
        print("🚩 Flag: NETSOS{c0ngrAtS_y0U_hAv3_unC0v3r3d_r3g1s7rY_p3rs1sT3nc3_4nD_r3m07e_sh3ll_a1l_1n_0n3}")
        print("=" * 80)


if __name__ == "__main__":
    main()
