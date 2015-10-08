== Fuku CTF ==

Fuku (pronounced "far queue") CTF is designed to fuck with people.

This is a boot2root. Import it in VirtualBox, using a Host Only adapter, or use an adapter that will assign it an IP address in the 192.168.56.0/24 range. It only likes having an IP address in that range.

Treat the box as if it was on the network. Don't try to do anything to it that you could only do with physical access, e.g. break into the BIOS or the Grub boot loader.

There are a few flag.txt files to grab. The final one is in the /root/ directory. However, the ultimate goal is to get a root shell.

== Scenario ==

"Bull was pissed when you broke into his Minotaur box. He has taken precautions with another website that he is hosting, implementing IDS, whitelisting, and obfuscation techniques. He is now taunting hackers to try and hack him, believing himself to be safe. It is up to you to put him in his place."

== Location ==

The VM is located at https://www.dropbox.com/s/e2x79z5ovqqsejg/Fuku.ova?dl=0 [File size: 2GB]

== Hints ==

1. Some scripting will probably be needed to find a useful port.
2. If the machine seems to go down after a while, it probably hasn't. This CTF isn't called Fuku for nothing!

Contact @RobertWinkel for more hints.
