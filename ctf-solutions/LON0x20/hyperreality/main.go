package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/binary"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"syscall"
	"time"
)

const blockSize = 16

var (
	flag      = mustEnv("FLAG") // contains lowercase letters, curly brackets, and underscores
	aesCipher = newAESCipher()
)

func handle(conn net.Conn) error {
	// create random IV
	iv, err := readBytes(rand.Reader, blockSize)
	if err != nil {
		return err
	}
	_, err = conn.Write(iv)
	if err != nil {
		return err
	}

	for {
		// read 4 bytes indicating the data length first
		data, err := readBytes(conn, 4)
		if err != nil {
			return err
		}
		length := binary.LittleEndian.Uint32(data)
		if length > 4096 {
			return nil
		}

		// read the data to be encrypted
		plaintext, err := readBytes(conn, int(length))
		if err != nil {
			return err
		}

		// append the secret
		plaintext = append(plaintext, []byte(flag)...)

		// encrypt it
		ciphertext := encrypt(plaintext, iv)

		// the IV for the next block is the end of the ciphertext for this block
		iv = ciphertext[len(ciphertext)-blockSize:]

		// send back the ciphertext length
		err = binary.Write(conn, binary.LittleEndian, uint32(len(ciphertext)))
		if err != nil {
			return err
		}

		// send back the ciphertext
		_, err = conn.Write(ciphertext)
		if err != nil {
			return err
		}
	}
}

func encrypt(plaintext, iv []byte) []byte {
	encrypter := cipher.NewCBCEncrypter(aesCipher, iv)
	padded := pad(plaintext)
	ciphertext := make([]byte, len(padded))
	encrypter.CryptBlocks(ciphertext, padded)
	return ciphertext
}

// pad appends bytes to data to make its length a multiple of block size.
// The value of each added byte is the total number of bytes added. For example, if we need
// to increase the length of data by 3, we add '\x03\x03\x03'.
// Note that the amount of padding added is in the range [1, blockSize], so some padding is always added.
func pad(data []byte) []byte {
	paddingLen := blockSize - (len(data) % blockSize)
	padding := make([]byte, paddingLen)
	for i := range padding {
		padding[i] = byte(paddingLen)
	}
	return append(data, padding...)
}

func newAESCipher() cipher.Block {
	key, err := readBytes(rand.Reader, 32)
	if err != nil {
		log.Fatalf("error: create cipher key: %v", err)
	}
	cipher, err := aes.NewCipher(key)
	if err != nil {
		log.Fatalf("error: set up cipher: %v", err)
	}
	return cipher
}

func readBytes(r io.Reader, n int) ([]byte, error) {
	b := make([]byte, n)
	_, err := io.ReadFull(r, b)
	return b, err
}

func mustEnv(key string) string {
	v, ok := os.LookupEnv(key)
	if !ok {
		panic(fmt.Sprintf("env %s not found", key))
	}
	return v
}

func main() {
	log.SetFlags(0)

	const addr = ":4000"
	log.Printf("listening on %s", addr)
	l, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatalf("error: %v", err)
	}
	defer l.Close()
	for {
		conn, err := l.Accept()
		if err != nil {
			log.Printf("error: %v", err)
			continue
		}
		go func() {
			defer conn.Close()
			log.Printf("connection from %s", conn.RemoteAddr())
			if err := checkTimeout(conn, handle(conn)); err != nil && err != io.EOF {
				log.Printf("error: %v", err)
			}
		}()
	}
}

func checkTimeout(conn net.Conn, err error) error {
	if ne, ok := err.(net.Error); ok && ne.Timeout() {
		conn.SetDeadline(time.Now().Add(time.Second))
		fmt.Fprintln(conn, "\nToo slow!")
		return nil
	}

	if oerr, ok := err.(*net.OpError); ok {
		if serr, ok := oerr.Err.(*os.SyscallError); ok && serr != nil && serr.Err == syscall.ECONNRESET {
			return nil
		}
	}
	return err
}
