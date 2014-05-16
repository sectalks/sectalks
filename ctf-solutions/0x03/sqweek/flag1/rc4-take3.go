package main

import (
	"crypto/rc4"
	"bufio" // bringing out the big guns
	."fmt"
	"os"
	"io"
)

var αβ = []byte("abcdefghijklmnopqrstuvxyz")

var data []byte

func printable(result []byte) (string, bool) {
	obscure := false
	s := ""
	for _, b := range(result) {
		switch {
		case b == 7: s += "\\a"
		case b == 8: s += "\\b"
		case b == 9: s += "\\t"
		case b == 10: s += "\\n"
		case b == 11: s += "\\v"
		case b == 12: s += "\\f"
		case b == 13: s += "\\r"
		case (b > 27) && (b < 127): s += string(b)
		default:
			obscure = true
			s += Sprintf("\\x%02x", b)
		}
	}
	return s, obscure
}

/* stripped from bf(), will need it again in a minute */
func trykey(key []byte) {
	cipher, err := rc4.NewCipher(key)
	if err != nil {
		panic(err)
	}
	result := make([]byte, len(data))
	cipher.XORKeyStream(result, data)
	s, obscure := printable(result)
	if !obscure {
		Println(string(key), s)
	}
}

func bf(index int, key []byte) {
	if index == len(key) {
		trykey(key)
		return
	}
	for _, c := range(αβ) {
		key[index] = c
		bf(index + 1, key)
	}
}

func main() {
	data = make([]byte, 256)
	n, err := os.Stdin.Read(data)
	Println("read ", n, "bytes")
	if err != nil {
		panic(err)
	}
	data = data[:n]
	if len(os.Args) > 1 {
		/* And here it is - I already used stdin for the encrypted
		 * data, so the simplest way to shoehorn a dictionary
		 * attack into the current structure is to accept a filename
		 * containing a list of words as the first argument */
		keylist, _ := os.Open(os.Args[1])
		rdr := bufio.NewReader(keylist)
		/* 'for' by itself is an infinite loop */
		for {
			line, err := rdr.ReadBytes('\n')
			if len(line) > 0 {
				/* strip newline from the string */
				if line[len(line) - 1] == '\n' {
					line = line[:len(line) - 1]
				}
				trykey(line)
			}
			if err != nil {
				if err == io.EOF {
					return
				}
				panic(err)
			}
		}
	} else {
		key := make([]byte, 6)
		bf(0, key)
	}
}


/*    OUTPUT
 * $ time go run rc4-take3.go <(grep '^......$' /usr/share/dict/cracklib-small) <input
 * read  16 bytes
 * murphy Invalid password
 * 
 * real   0m0.492s
 * user   0m0.427s
 * sys    0m0.097s
 */


/*    COMMENTS
 * So half second to execute the dictionary attack (6945 words) -
 * and that includes compilation of the go code. In this smaller
 * set of  keys there's only a single key that has a "printable"
 * result, which is the password we're looking for.
 *
 * If you're still looking at the command I used to run it and
 * thinking WTF I'll break it down for you:
 *
 * "foo <(bar)" is a bash construct that allocates a pipe, passes
 * the _filename_ of the pipe's output end (eg. /dev/fd/63) as an
 * argument to the 'foo' command, and attaches the pipe's input
 * end to stdout of the 'bar' command.
 *
 * What I've done here is equivalent to:
 * $ grep '^......$' /usr/share/dict/cracklib-small >/tmp/6-letter-words
 * $ go run rc4-take3.go /tmp/6-letter-words <input
 *
 * but without the temporary file, and with grep running in
 * parallel to my go program.
 */
