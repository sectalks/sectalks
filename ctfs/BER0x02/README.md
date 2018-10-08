# Challenge #1: randomware
- Ransomware
- Made by cheese02
- Has two versions
    - With debug symbols (easy)
    - Stripped (hard)
- Located in `ELF/binaries`

## ELF
1. What type of ELF file is this?
2. What is the value of `Elf64_Ehdr.e_version` in this file?
3. What is the segment type that contains the section `.init_array`?
   
## Binary
1. What is the virtual address of the entrypoint of the binary?
2. What is the decryption key?
3. What algorithm is used for encryption?


======================================================================


# Challenge #2: malificent.exe
- Live malware
- Ripped from *Practical Malware Analysis*

## PE
1- For section `.rsrc`, how much space does this section occupy on disk?
2- What is the virtual address of the first code that executes in this binary?
3- What is the total amount of memory this binary will reserve in process memory?

## Binary
1. When was this program compiled?
2. Do any imports hint at this program’s functionality? If so, which imports are they and what do they tell you?
3. What host- or network-based indicators could be used to identify this malware on infected machines?
4. This file has one resource in the resource section. What is it?


# Credits
Made by Abdullah Obaied (cheese02)
