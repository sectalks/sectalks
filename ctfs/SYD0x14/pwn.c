
/* Source: http://212.71.244.194/ds/pwn/ */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdlib.h>
#include <error.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
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
  int fd;
  char b[50];

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

  printf("Getting to this point means you deserve a flag: ");
  fd = open("/home/pwn/flag.txt", O_RDONLY);
  read(fd, &b, sizeof(b));
  printf("%s\n", b);
  close(fd);
  
  return 0;
}
