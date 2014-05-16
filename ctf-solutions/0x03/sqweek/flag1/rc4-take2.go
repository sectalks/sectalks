package main

import (
	"crypto/rc4"
	."fmt"
	"os"
)

var αβ = []byte("abcdefghijklmnopqrstuvxyz")

/* ok the greek was funny _once_ :) */
var data []byte

/* go supports multiple return values, which makes it easy to add
 * a flag when obscure characters are detected, so we can suppress
 * crappy results altogether and avoid overworking grep. */
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

func bf(index int, key []byte) {
	if index == len(key) {
		cipher, err := rc4.NewCipher(key)
		if err != nil {
			panic(err)
		}
		result := make([]byte, len(data))
		cipher.XORKeyStream(result, data)
		str, obscure := printable(result)
		if !obscure {
			Println(string(key), str)
		}
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
	key := make([]byte, 6)
	bf(0, key)
}

/*    OUTPUT
 * $ go run rc4-take2.go <input
 * read  16 bytes
 * aameaj >9:[h~,,!|#%!\v0P
 * ackkbs >xgM>~0v;b @CKG
 * ajcdeh XdrMTG(?S%#C)\b@
 * ajkirk F0Rl.`TR\Ys?ut8k
 * ajycyd sHx4(#i'!\r'70OX
 * ayiqfi ,s|af~!=K@ON-Xs6
 * aysctm et{xU<y'3P:CH`$Y
 * bcfthy r:\i;;7(}6Oi6^E
 * ... etc etc
 */

/*    COMMENTS
 * This one runs much faster. Still going to take on the order
 * of 2 hours to finish, and I have a lot of crappy results to
 * sift through... I have an idea to speed things up and reduce
 * the amount of results at the same time. */
