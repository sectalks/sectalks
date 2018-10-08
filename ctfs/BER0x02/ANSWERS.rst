Challenge #1: randomware
========================

ELF
---
1. What type of ELF file is this?
2. What is the value of `Elf64_Ehdr.e_version` in this file?
3. What is the segment type that contains the section `.init_array`?
   
Answers to "ELF"
----------------
1. `ET_DYN` or `DYN`
2. 1
3. `PT_LOAD`

Binary
------
1. What is the virtual address of the entrypoint of the binary?
2. What is the decryption key?
3. What algorithm is used for encryption?

Answers to "Binary"
-------------------
1. `0x00001200`. Taken from `rabin2 -ee randomware`
2. `bunnyfoofoo`. Its also the encryption key
3. XOR


======================================================================


Challenge #2: malificent.exe
============================

PE
--
1- For section `.rsrc`, how much space does this section occupy on disk?
2- What is the virtual address of the first code that executes in this binary?
3- What is the total amount of memory this binary will reserve in process memory?

Answers to "PE"
---------------
1. 4096
2. 0x405000
3. OptionalHeader.SizeOfImage: 0x6000

Binary
------
1. When was this program compiled?
2. Do any imports hint at this program’s functionality? If so, which imports are they and what do they tell you?
3. What host- or network-based indicators could be used to identify this malware on infected machines?
4. This file has one resource in the resource section. What is it?

Answers to "Binary"
-------------------
1. According to the file header, this program was compiled in August 2019.
Clearly, the compile time is faked, and we can’t determine when the file
was compiled.

2. The imports from advapi32.dll indicate that the program is doing something
with permissions. The imports from *WinExec* and *WriteFile* tell us that the program 
writes a file to disk and then executes it. There are also imports for reading information
from the resource section of the file.

3. The string `\system32\wupdmgr.exe` indicates that this program could create
or modify a file at that location. The string www.malwareanalysisbook.com/
updater.exe probably indicates where additional malware is stored, ready
for download.

4. A packed PE
