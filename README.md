# 🐉 Jay’s CTF Playground
### Cybersecurity Challenge Development

Hi! I'm **Jaysen Lestari**, a Computer Science student at **Universitas Indonesia** with a strong passion for **cybersecurity**, especially in **CTF competitions**, **digital forensics**, **web exploitation**, and **cryptography**.

This repository contains a collection of **CTF challenges that I designed and developed** for various events such as **Pekan Ristek 2025**, **RISTEK 2026 Open Recruitment**, and **COMPFEST17**.

Each challenge typically includes:

- **public/** → files given to participants  
- **src/** → challenge source / generation scripts  
- **writeup/** → intended solution and explanation  

This repository serves as my **personal challenge development archive**, where I design layered problems inspired by real-world scenarios and modern attack techniques.

---

# 📂 Repository Structure
```
challanges/
├── crypto
├── forensics
└── web
```

Each category contains multiple challenges.

---

# 🧩 Challenges

| Category  | Challenge             | Difficulty  | Description                                                                                                                                                                                           | Link                                           |
| --------- | --------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Forensics | Dear bf               | Beginner    | Simple file recovery challenge. Participants brute-force a ZIP password using `rockyou` and repair corrupted file signatures to recover the flag.                                                     | [Open](./challanges/forensics/Dear%20bf)       |
| Forensics | mimpi                 | Beginner    | Network traffic analysis challenge where a binary file is reconstructed from WebSocket traffic inside a PCAP and extracted from a password-protected ZIP archive.                                     | [Open](./challanges/forensics/mimpi)           |
| Forensics | p-info                | Easy     | EVTX log analysis challenge involving suspicious Base64 data exfiltration. Participants reconstruct a PDF and analyze embedded obfuscated JavaScript to recover multiple flag parts.                  | [Open](./challanges/forensics/p-info)          |
| Forensics | hulk                  | Easy-Medium      | Memory forensics challenge using **Volatility** to recover artifacts from Linux memory. Players reconstruct encrypted files, extract AES keys, and reverse an associated binary.                      | [Open](./challanges/forensics/hulk)            |
| Forensics | nyawit                | Medium | Multi-layer Windows forensic investigation combining **registry analysis, EVTX logs, browser history, $J journal, prefetch artifacts**, and malware analysis to reconstruct attacker activity.        | [Open](./challanges/forensics/nyawit)          |
| Forensics | update-required       | Hard   | Full attack-chain investigation involving **PCAP analysis, ransomware reverse engineering, AES decryption, clipboard forensics, and MetaMask vault recovery** to unlock the final encrypted document. | [Open](./challanges/forensics/update-required) |
| Web       | Cryptweb              | Medium        | Stored XSS leads to exfiltration of internal configuration data. Players must combine **XSS, AES-CBC bit-flipping, and HMAC forgery** to forge an admin session cookie and access `/admin/dashboard`. | [Open](./challanges/web/Cryptweb)              |
| Web       | dark-side-of-asteroid | Easy       | Web exploitation challenge combining **DNS rebinding**, localhost access bypass, and **SQL injection** to exploit an internal admin search endpoint through an admin bot.                             | [Open](./challanges/web/dark-side-of-asteroid) |
| Crypto    | baby-leaked           | Easy–Medium | RSA challenge with partial prime leakage. Players must recover the missing bits of `p` using **Coppersmith’s small root attack** and handle a non-coprime public exponent (`e = 16`).                 | [Open](./challanges/crypto/baby-leaked)        |

---

# 🔗 Connect With Me

- LinkedIn: http://www.linkedin.com/in/jaysen-lestari
- Blog: https://jaysenlestari.github.io/

Happy hacking! 🦊🔐