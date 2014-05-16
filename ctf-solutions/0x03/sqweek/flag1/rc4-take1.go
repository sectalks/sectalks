package main

import (
	"crypto/rc4" // luckily rc4 is in standard library
	."fmt"
	"os"
)
/* import ."fmt" gets symbols into the current namespace
 * (so I can write Println instead of fmt.Println) */

/* english identifiers are for pussies */
var αβ = []byte("abcdefghijklmnopqrstuvxyz")

/* the captured encrypted data */
var δ []byte

func ρ(σ []byte) (string) {
	Σ := ""
	for _, θ := range(σ) {
		switch {
		case θ == 7: Σ += "\\a"
		case θ == 8: Σ += "\\b"
		case θ == 9: Σ += "\\t"
		case θ == 10: Σ += "\\n"
		case θ == 11: Σ += "\\v"
		case θ == 12: Σ += "\\f"
		case θ == 13: Σ += "\\r"
		case (θ > 27) && (θ < 127): Σ += string(θ)
		default: Σ += Sprintf("\\x%02x", θ)
		}
	}
	return Σ
}

/* recursive brute-force implementation */
func βφ(ι int, κ []byte) {
	if ι == len(κ) {
		ξ, err := rc4.NewCipher(κ)
		if err != nil {
			panic(err)
		}
		Δ := make([]byte, len(δ))
		ξ.XORKeyStream(Δ, δ)
		Println(string(κ), ρ(Δ))
		return
	}
	for _, θ := range(αβ) {
		κ[ι] = θ
		βφ(ι + 1, κ)
	}
}

func main() {
	δ = make([]byte, 256)
	Ν, err := os.Stdin.Read(δ)
	Println("read ", Ν, "bytes")
	if err != nil {
		panic(err)
	}
	δ = δ[:Ν]
	κ := make([]byte, 6)
	βφ(0, κ)
}

/*    OUTPUT
 * $ go run rc4-take1.go <input | grep -v '\\x'
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
 * Ok so spewing the results for EVERY key to stdout means
 * that grep needs an entire cpu to do string matching. Not
 * the most efficient approach, guess I have to re-evaluate
 * my design.
 */
