# Writeup <mimpi>
Gunakan tshark untuk mengekstrak binary filesnya :
```bash
tshark -r captured.pcap -Y "websocket && data.data" -T fields -e data.data > file_hex.txt
```
Setelah itu ubah hex dump tadi menjadi raw :
```bash
tr -d '\n' < file_hex.txt | xxd -r -p > file.bin
```
Setelah di cek menggunakan command ``file file.bin``, file tersebut merupakan zip file. Karena zip file tersebut ada password, gunakan rockyou untuk melakukan bruteforcing password dan akan ditemukan password : ``all day i dream about you``. Setelah itu unzip dan didapatkan sebuah file png, ubah ukuran file pngnya, dan berhasil mendapatkan flag.