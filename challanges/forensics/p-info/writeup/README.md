# Writeup <Judul Soal>
Disini diberikan file evtx, tinggal cari event dengan src ShellOps karena itu sangat mencurigakan terlihat bahwa adanya data-data yang dikirim dalam base64 yang terdiri dari part1-part50, masing-masing part terdiri dari 5 part chunk, dump semua data tersebut kemudian gabung dan decode dari base64, maka kamu akan menemukan file pdf nya. Part1 dari flag akan ditemukan dalam pdf tersebut.
Part2 dari flag dengan melakukan command `pdfinfo -js file_name`, akan ditemukan script js yang telah diobfuscated dengan memakai obfuscator.io, lakukan deobfuscated dan akan mendapatkan :
```javascript
const bytes = "50 41 52 54 20 32 20 3a 20 54 31 6e 67 67 61 6c 5f 33 6b 73 74 72 41 6b 5f 74 33 52 55 73 5f 69 6e 66 6f 2d 69 6e 66 6f 0d 0a".split(/\s+/);
function pad3(_0x49fcd0) {
  const _0x1630de = String(_0x49fcd0);
  return _0x1630de.length >= 0x3 ? _0x1630de : '0'.repeat(0x3 - _0x1630de.length) + _0x1630de;
}
const padded = [];
for (let i = 0x0; i < bytes.length; i++) {
  const num = parseInt(bytes[i], 0x10);
  const paddedNum = pad3(num);
  padded.push(paddedNum);
}
const joined = padded.join('');
console.log(joined);
```
Selanjutnya part3 dapat ditemukan dengan `pdfinfo nama_file` , maka akan terlihat sebuah base64 yang ternyata merupakan script powershell:
```Poweshell script
$payload="9esFBrKoybYyAxUxTiL4BTY9QkggIzA4a0x5UlejVw=="
$enc=[Convert]::FromBase64String($payload)
$sb=New-Object System.Text.StringBuilder
for($i=0;$i -lt $enc.Length;$i++){
    $val=$enc[$i]
    $step1=$val-($i*7)
    $wrapped=$step1 -band 0xFF
    $orig=($wrapped -bxor 0xA5) -band 0xFF
    [void]$sb.Append([char]$orig)
}
Write-Output $sb.ToString()
```
Jalankan saja kode tersebut di powershell dan anda akan mendapatkan part3 nya.
