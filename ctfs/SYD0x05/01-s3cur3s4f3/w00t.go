/*
 * I'm getting really tired of `su`s shit.
 * You physically can't get a tty inside `docker exec`.
 */

package main

import (
	"fmt"
	"os"
	"bufio"
	"strings"
	"syscall"
	"runtime"
)

/* NOTE: Make sure you `chmod -r` this binary. */
const flag = "br1ng1ng_b4ck_hunter2"

func main() {
	fmt.Fprintf(os.Stdout, "[?] Enter flag{...} to w00t w00t: ")
	os.Stdout.Sync()
	runtime.LockOSThread()

	val, err := bufio.NewReader(os.Stdin).ReadString('\n')
	if err != nil {
		fmt.Fprintf(os.Stderr, "[!] error while reading flag: %s\n", err)
		os.Exit(1)
	}

	val = strings.TrimSpace(val)
	if val != flag {
		fmt.Fprintf(os.Stderr, "[-] m33p m33p failed to g3t gl4d0s :(\n")
		os.Exit(1)
	}

	fmt.Fprintf(os.Stdout, "[+] w00t w00t g0t gl4d0s :)\n")

	/*
	 * We need to use dash because bash is broken.
	 * No that isn't a joke, and yes it's cancer.
	 */
	syscall.Exec("/bin/dash", []string{"-dash"}, os.Environ())
}
