#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
  printf("This is a sample KRL executable.\n");
  unlink(argv[0]);
  return 0;
}
