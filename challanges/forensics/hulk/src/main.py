def main():
    print("\n⚠️  HULKKKKK SMASHHHHHHH ⚠️")

    answers = [
        "5.15.0-170",
        "10.5.123.238_80_netsos",
        "/home/tipsen/Downloads/netsos",
        "a95640950eeaccdd09333ccad0c3db841fdb7c810bbde34c113279e63119dcb6",
        "http://10.5.123.238:8080/api/v1/get_config",
        "0634d24804cd0e5e9f6d543b95e7caedd9b118c3274723081a0983d09cd90307_th1s_1s_th3_IVVV",
        "README.txt.enc,SuratEdaranLiburPuasa2026UniversitasIndonesia.pdf.enc,imej.jpg.enc,mydiary.pdf.enc",
        "864758"
    ]

    questions = [
        ("To start the investigation, identify the exact version of the Linux kernel running on the victim's machine.",
        "X.X.X-XXX (e.g., 6.2.15-300)"),
        ("The victim downloaded a malicious executable from an external server. What is the source IP address, port number, and the exact filename of the downloaded malware?",
         "IP_Port_Filename (e.g., 192.168.1.10_8000_malware.elf)"),
        ("What is the full absolute path where the malicious executable was saved and executed from on the victim's machine?",
         "/path/to/directory/filename"),
        ("To check for indicators of compromise (IOC), what is the SHA-256 hash of the malicious executable?",
         "SHA256_HASH"),
        ("Upon execution, the malware reaches out to an external Command and Control (C2) server to retrieve additional data required for its payload. What is the full URL of the specific endpoint requested by the malware?",
         "http://IP:Port/path (e.g., http://10.0.0.5:8080/api/v1/get_config)"),
        ("By analyzing the memory dump and the network traffic, extract the cryptographic parameters used by the ransomware. What are the AES Key and the Initialization Vector (IV)?",
         "Key_IV (e.g., 0634d2...0304_abcdefgh)"),
        ("Identify all the files that were successfully encrypted by the ransomware in the victim's system. List the exact filenames separated by commas, sorted in lexicographical (alphabetical) order",
         "Format: filenameA.enc,filenameB.enc,... (e.g., A_file.txt.enc,Z_file.png.enc,a_file.pdf.enc,...)"),
        ("Use the extracted cryptographic parameters to decrypt the compromised files. After successfully decrypting the target file, what is the secret PIN written inside it?",
         "PIN (e.g., 1234)")
    ]

    correct_count = 0

    for i, (question, fmt) in enumerate(questions):
        print("\n" + "-" * 80)
        print(f"Question {i+1}/{len(questions)}")
        print(question)
        print(f"Format: {fmt}")
        print("-" * 80)

        user_answer = input("Answer: ").strip()
        expected_answer = answers[i]

        is_correct = user_answer == str(expected_answer)
        if is_correct:
            correct_count += 1
            print("Correct!")
        else:
            print("Incorrect! Investigation terminated.")
            return
        
    if correct_count == len(questions):
        print("\n" + "=" * 80)
        print("🚩 Flag: NETSOS{bu1k_3xtrac7orrr_15_v3rY_p0w3rfu1111}")
        print("=" * 80)


if __name__ == "__main__":
    main()