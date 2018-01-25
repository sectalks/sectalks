// 
// Sectalks London CTF0x10 - January 2018
// Patrick Coleman <blinken@gmail.com>
//
// For an authentic experience compile on GNU Linux with
//
//     gcc -o forever -fno-stack-protector -O0 --std=c99 forever.c
//
// Only the compiled binary was provided for the CTF. Contestents are expected
// to use a debugger (example shown was gdb) to make the binary produce three
// flags. Modification of instructions in memory is expected/required.
//
// Apologies for the code below.
//

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <error.h>
#include <string.h>
#include <sys/mman.h>

// count binary ones in the activation §code
static inline int check_activation_code(int code) {
  if (code < 10000000) return 1; // must be 8 digits

  int ones = 0;
  int useless;
  int mod2 = code % 2;
  int loop;
  while (code > 0) {
    ones += code & 0x1;
    code >>= 1;

    // obfuscation
    loop = 4;
useless:
    useless = 0;
    while (useless < code*30) useless++;
    for (int i=0; i<useless; i++) {}
    loop--;
  }

  //printf("DEBUG activation: %d ones in code, mod2 = %d\n", ones, mod2);
  if ((ones == 10) && (mod2 == 0)) return 0; // code must have ten bits set and be divisible by 2
  if (loop > 0) goto useless;

  return 1;

}

// encode a string by xoring it with a random key, so it's not obvious in a
// debugger
unsigned const char key[] = {0x15, 0x65, 0x12, 0x91, 0x93, 0x33, 0x71, 0x81};
void px(unsigned char *buf) {
  printf("{");
  for (int i=0; i<strlen(buf); i++) {
    printf("0x%02x, ", buf[i] ^ key[i % 8]);
  }
  printf("}\n");
}

// decode a string encoded using px
void print_flag(unsigned char *buf, int len) {
  int loop, useless;

  printf("flag: ");
  for (int i=0; i<len; i++) {
    printf("%c", buf[i] ^ key[i % 8]);

    loop = 4;
useless:
    useless = 0;
    while (useless < i*30) useless++;
    for (int i=0; i<useless; i++) {}
    loop--;
  }

  if (loop > 0) goto useless;
  printf("\n");
}

// challenge three: this function is modified by main(), so the version in
// memory will be different to the version on disk
unsigned char flag3[] = {0x5c, 0x11, 0x32, 0xe6, 0xf2, 0x40, 0x51, 0xf5, 0x7d, 0x00, 0x32, 0xfc, 0xf2, 0x41, 0x1a, 0xa1, 0x7a, 0x03, 0x32, 0xf0, 0xb3, 0x51, 0x10, 0xf3, 0x77, 0x04, 0x60, 0xf8, 0xf2, 0x5d, 0x51, 0xf5, 0x7a, 0x45, 0x76, 0xf4, 0xe0, 0x47, 0x03, 0xee, 0x6c, 0x45, 0x61, 0xfe, 0xfe, 0x56, 0x05, 0xe9, 0x7c, 0x0b, 0x75, 0xb1, 0xfc, 0x5d, 0x14, 0xa1, 0x76, 0x0a, 0x67, 0xfd, 0xf7, 0x13, 0x1f, 0xee, 0x61, 0x45, 0x67, 0xff, 0xf7, 0x56, 0x03, 0xf2, 0x61, 0x04, 0x7c, 0xf5, 0xbd};
int THE_FINAL_COUNTDOWN() {
  volatile uint8_t n = 50;

  printf("\nTHE FINAL COUNTDOWN\n");
  for (; n > 0; n--) {
    printf("%d...\n", n);
    if (n == 42) {
      // It was the mark of a barbarian to destroy something one could not understand.
      print_flag(flag3, sizeof(flag3));
      exit(0);
    }
  }

  error(1, 0, "Bad hacking detected!");
}

int main() {
  // challenge one: an infinite loop
  printf("Starting up (this may take a while)...\n\n");
  uint8_t i = 0;
  while (i != 1) {} // change to 0

  // flag: When in doubt, say nothing and move on.
  unsigned char flag1[] = {0x42, 0x0d, 0x77, 0xff, 0xb3, 0x5a, 0x1f, 0xa1, 0x71, 0x0a, 0x67, 0xf3, 0xe7, 0x1f, 0x51, 0xf2, 0x74, 0x1c, 0x32, 0xff, 0xfc, 0x47, 0x19, 0xe8, 0x7b, 0x02, 0x32, 0xf0, 0xfd, 0x57, 0x51, 0xec, 0x7a, 0x13, 0x77, 0xb1, 0xfc, 0x5d, 0x5f};
  print_flag(flag1, sizeof(flag1));

  printf("Enter activation code [XXXXXXXX]: ");
  uint8_t canary = 42;
  char code_s[8];
  uint8_t canary2 = 42;

  fgets(code_s, 14, stdin);
  printf("\n");

  // attempt to detect overflows of code_s
  if ((canary != 42) || (canary2 != 42)) error(1, 0, "Hacking detected!");

  // challenge two: the entered activation code is verified by the obfuscated
  // function check_activation_code. The 
  if (check_activation_code(atoi(code_s))) error(1, 0, "Activation failed.");

  printf("Activation succeeded.\n");

  // flag: It has yet to be proven that intelligence has any survival value.
  unsigned char flag2[] = {0x5c, 0x11, 0x32, 0xf9, 0xf2, 0x40, 0x51, 0xf8, 0x70, 0x11, 0x32, 0xe5, 0xfc, 0x13, 0x13, 0xe4, 0x35, 0x15, 0x60, 0xfe, 0xe5, 0x56, 0x1f, 0xa1, 0x61, 0x0d, 0x73, 0xe5, 0xb3, 0x5a, 0x1f, 0xf5, 0x70, 0x09, 0x7e, 0xf8, 0xf4, 0x56, 0x1f, 0xe2, 0x70, 0x45, 0x7a, 0xf0, 0xe0, 0x13, 0x10, 0xef, 0x6c, 0x45, 0x61, 0xe4, 0xe1, 0x45, 0x18, 0xf7, 0x74, 0x09, 0x32, 0xe7, 0xf2, 0x5f, 0x04, 0xe4, 0x3b};
  print_flag(flag2, sizeof(flag2));

  // challenge three: self-modifying code (of variable effectiveness). Trips up
  // people who only use static analysis and do not run the program
  //
  // get a pointer to the function THE_FINAL_COUNTDOWN(), and remove memory
  // protection with mprotect. Apparently calls to mprotect must be aligned to
  // the start of the page. Much of the below is stolen from SO
  unsigned char *ptr = (unsigned char *)&THE_FINAL_COUNTDOWN;
  int page_size;
  page_size = getpagesize();

  if (mprotect(ptr - ((unsigned long)ptr % page_size), page_size, PROT_READ | PROT_WRITE | PROT_EXEC) != 0) {
    perror("");
    exit(1);
  }

  // Search for the constant '50'
  while (*ptr != 50) {
    ptr++;
    //printf("%p = %02x (%02d)\n", ptr, *ptr, *ptr);
  }

  // Change 50 to 10, so the function will never succeed
  //printf("Modifying address %p\n", ptr);
  ptr[0] = 10;

  // Call the modified function
  THE_FINAL_COUNTDOWN();
}

