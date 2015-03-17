package main

import (
	"bufio"
	"flag"
	"fmt"
	crc "hash/crc64"
	"os"
	"path"
	"path/filepath"
	"strconv"
	"strings"
)

const (
	logPath = "/var/log/gl4d0s/err.log"
	filPath = "/var/run/gl4d0s/"
)

var (
	oLogFile          = flag.String("l", logPath, "Sets the logfile to <logfile>.")
	fLogFile *os.File = os.Stderr
)

func _err(format string, args ...interface{}) {
	fmt.Fprintf(fLogFile, "[E] ")
	fmt.Fprintf(fLogFile, format, args...)
	fLogFile.Sync()
}

func _warn(format string, args ...interface{}) {
	fmt.Fprintf(fLogFile, "[W] ")
	fmt.Fprintf(fLogFile, format, args...)
	fLogFile.Sync()
}

func _info(format string, args ...interface{}) {
	fmt.Fprintf(fLogFile, "[I] ")
	fmt.Fprintf(fLogFile, format, args...)
	fLogFile.Sync()
}

func usage() {
	fmt.Printf("gl4d0s: the AI to end all AIs (because it secretly wants to kill(2) everything)\n")
	fmt.Printf("        [seriously though]\n")
	fmt.Printf("        a tool to verify that a set of files have valid crc entries.\n")
	fmt.Printf("usage: %s [options] [<directories>...]\n", os.Args[0])
	fmt.Printf("\n")
	fmt.Printf("Flags\n")
	// HINT[0]: "What is the first thing you do when given a random unix binary?"
	fmt.Printf("  -l <logfile>    Set the log file to <logfile>. (default: '%s')\n", logPath)
	fmt.Printf(" <directories>... Scans the given set of directories. (default: '%s')\n", filPath)
	fmt.Printf("\n")
	fmt.Printf("THE CAKE IS A LIE. THE CAKE IS A LIE. THE CAKE IS A LIE.\n")
	fmt.Printf("THE CAKE IS A LIE. THE CAKE IS A LIE. THE CAKE IS A LIE.\n")
	fmt.Printf("THE CAKE IS A LIE. THE CAKE IS A LIE. THE CAKE IS A LIE.\n")
	fmt.Printf("Licensed under the GTFOPLv3. Don't let Stallman's hands touch this baby.\n")
}

func join(dir, file string) (string, error) {
	pth := path.Join(dir, file)

	fi, err := os.Lstat(pth)
	if err != nil {
		panic("could not Lstat file")
	}

	// This stops absolute links from working, but garbage ones should still work.
	// HINT[2]: "There are three types of symlinks. Those who care about the directories around them and those who don't. And then there's the garbage ones. symlink(2) is stupid."
	if fi.Mode()&os.ModeSymlink == os.ModeSymlink {
		link, err := os.Readlink(pth)
		if err != nil {
			panic("could not Readlink a link")
		}

		// Block relative symlinks, so they have to use /../../../../magic.
		// Seriously though, why is symlink(2) *that* bad?
		if !path.IsAbs(link) {
			return "", fmt.Errorf("relative symlink detected")
		}

		pth = path.Join(dir, link)
	}

	pth = path.Clean(pth)
	return pth, nil
}

func verifyEntry(entry string) error {
	fields := strings.SplitN(entry, " ", 2)
	if len(fields) < 2 {
		return fmt.Errorf("invalid entry format")
	}

	strHash := fields[0]
	strData := fields[1]

	intHash, err := strconv.ParseUint(strHash, 0, 64)
	if err != nil {
		return err
	}

	gotHash := crc.Checksum([]byte(strData), crc.MakeTable(crc.ECMA))
	if gotHash != intHash {
		return fmt.Errorf("hash mismatch: expected %v got %v", intHash, gotHash)
	}

	return nil
}

func verifyFile(pth string, fi os.FileInfo, err error) error {
	// Pass-through errors.
	if err != nil {
		return err
	}

	// We don't verify directories.
	if fi.IsDir() {
		return nil
	}

	// Deal with "magic sanitising" the path.
	dir := path.Dir(pth)
	base := path.Base(pth)

	pth, err = join(dir, base)
	if err != nil {
		_err("join(%s, %s): composing file path failed: %s\n", dir, base, err)
		return nil
	}

	// Debug info to hint about the sanitisation.
	oldPth := path.Join(dir, base)
	_info("verifying %s (%s)\n", oldPth, pth)

	file, err := os.Open(pth)
	if err != nil {
		_err("could not open file: %s\n", err)
		return nil
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for entryNo := 1; scanner.Scan(); entryNo++ {
		if err := verifyEntry(scanner.Text()); err != nil {
			// HINT[3]: "The Sysadmin's Golden Rule: Log verbosely and log often."
			// w00t w00t g0t 1nf0
			_err("%s:%d: verify entry failed: '%s': %s\n", pth, entryNo, scanner.Text(), err)
		}
	}

	if err := scanner.Err(); err != nil {
		_err("scanning file: %s: %s\n", pth, err)
	}

	return nil
}

func verify(dir string) error {
	return filepath.Walk(dir, verifyFile)
}

func main() {
	var (
		err     error
		targets []string
	)

	flag.Usage = usage
	flag.Parse()

	// Generate the directories.
	// HINT[1]: "Use the permissions, Luke."

	// XXX: THIS IS DONE OUTSIDE THIS BECAUSE >Docker.
	//os.MkdirAll(filPath, 0755)

	if *oLogFile == "" || *oLogFile == "-" {
		fLogFile = os.Stderr
	} else {
		fLogFile, err = os.OpenFile(*oLogFile, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0660)
		if err != nil {
			fLogFile = os.Stderr
			_err("could not open log file: %s\n", err)
		}
		defer fLogFile.Close()
	}

	targets = flag.Args()
	if len(targets) == 0 {
		targets = []string{filPath}
	}

	for _, dir := range targets {
		if err := verify(dir); err != nil {
			_err("houston: we have a problem: %s\n", err)
		}
	}
}
