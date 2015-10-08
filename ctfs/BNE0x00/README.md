== Intro ==

Minotaur is a boot2root CTF. Once you load the VM, treat it as a machine you can see on the network, i.e. you don't have physical access to this machine. Therefore, tricks like editing the VM's BIOS or Grub configuration are not allowed. Only remote attacks are permitted.
There are a few flag.txt files around to grab. /root/flag.txt is your ultimate goal.

This CTF has a couple of fairly heavy password cracking challenges, and some red herrings.

I suggest you use VirtualBox with a Host Only adapter to run Minotaur fairly painlessly.

The VM will assign itself a specific IP address (in the 192.168.56.0/24 range). Do not change this, as the CTF will not work properly without an IP address of 192.168.56.X.

If you load the .ova file in VirtualBox, you can see this machine from another VirtualBox machine with a "Host Only" network adapter.
You can see the machine from VMWare Workstation by:
- Going into Virtual Network Editor and changing the VMnet0 network to "Bridged to: VirtualBox Host-Only Ethernet Adapter".
- Setting your VMWare network adapter to Custom (VMnet0)
- If necessary, resetting your network adapter (e.g. ifdown eth0 && ifup eth0) so that you get a 192.168.56.0/24 address.

The VM is located here: https://www.dropbox.com/s/zyxbampga87nqv3/minotaur_CTF_BNE0x00.ova?dl=0 [File size: 691MB]

Contact @RobertWinkel for hints.
