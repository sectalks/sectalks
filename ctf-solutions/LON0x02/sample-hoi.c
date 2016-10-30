#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
  printf("This is a sample HOI executable.\n");
  unlink(argv[0]);
  return 0;
}
