# Update Required

by jay

---

## Flag

```
COMPFEST17{c0ngr@tulat1on_you_hav3_found_the_s3cret_and_here_is_y0ur_r3ward} 
```

## Description
A researcher in Mondstadt’s tech division received an urgent-looking HTML file, claiming to be a critical security patch. Trusting its source, they executed antivirus.exe and moments later, a secret PDF file disappeared.

The PDF contained a confidential override PIN tied to the Vision Distribution Network. To protect it, the researcher locked the PDF with their wallet’s seed phrase (exported from a Chrome extension), joined with an underscore (_) as the password.

Although the wallet vault file remains on disk, the password to unlock it has since been lost. Fortunately, there’s a lead: the researcher once copied the vault password to clipboard.

Zip password : soalinigasusahkokxixixixi

## Difficulty
Tingkat kesulitan soal: medium-hard

## Tags
rust-ransomware, clipboard-forensics, metamask, pcap-analysis

## Notes
This challenge was created for the COMPFEST 17 Qualification Round as a simple yet well-structured introduction to digital forensics (DFIR).
Although designed to be beginner-friendly, it still incorporates key components of modern DFIR workflows—such as PCAP analysis, malware/ransomware behavior, clipboard artifact recovery, and browser vault forensics.

This is also the first CTF challenge I’ve ever built, and I’m genuinely proud of how it turned out.
