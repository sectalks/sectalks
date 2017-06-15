
/* Source: http://212.71.244.194/ds/pwn/ */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdlib.h>
#include <error.h>
#include <sys/mman.h>
#include <errno.h>
#include <limits.h>

void err_exit(char *e) {
  fprintf(stderr, "%s\n", e);
  _exit(1);
}

char* getln(void) {
  char *buf = NULL;
  size_t len = 0;
  if (getdelim(&buf, &len, '\n', stdin) <= 0) {
    err_exit("getdelim() failed");
  }
  return buf;
}

int main(void) {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);

  printf("Quote of the day v0.3. Answer a few questions to get one\n");

  printf("Your double number: ");
  char *buf = getln();

  double d = strtod(buf, NULL);
  if (errno != 0) {
    err_exit("strtold() failed");
  }
  /* Is there any IEEE floating point number which can pass those checks? */
  if (d <= 42.0l) {
    err_exit("d is too low");
  }
  if (d > 42.0l) {
    err_exit("d is too high");
  }

  printf("Your integer number: ");
  buf = getln();

  long l = strtol(buf, NULL, 0);
  if (errno != 0) {
    err_exit("strtol() failed");
  }
  if (l < 0) {
    l = -l;
  }  
  l %= 3;
  /* number%3 results in either 0, 1 or 2. So, we're safe here. Most likely :) */
  if (l == 0) {
    err_exit("Your quote: Never miss a chance to keep your mouth shut");
  }
  if (l == 1) {
    err_exit("Your quote: I'm still an atheist, thank God");
  }
  if (l == 2) {
    err_exit("Your quote: Nothing ever goes away");
  }

  printf("Getting to this point is not technically feasible. I might as well execute your asm code now: ");
  
  void (*m)(void) = mmap(NULL, 4096, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
  if (m == MAP_FAILED) {
    err_exit("mmap() failed");
  }
  read(0, m, 4096);

  if (memmem(m, 4096, "\x0F\x05", 2)) {
    err_exit("No 'syscall' instruction allowed");
  }
  if (memmem(m, 4096, "\xCD\x80", 2)) {
    err_exit("No 'int 0x80' instruction allowed");
  }
  if (memmem(m, 4096, "\x0F\x07", 2)) {
    err_exit("No 'sysret' instruction allowed");
  }
  if (mprotect(m, 4096, PROT_EXEC|PROT_READ) == -1) {
    err_exit("mprotect() failed");
  }

  m();
  return 0;
}
