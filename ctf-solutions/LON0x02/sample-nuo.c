#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
  printf("This is a sample NUO executable.\n");
  printf("\n");
  printf(" ___\n");
  printf("(__ `-._                _____\n");
  printf("   `-._ `-._          .'     `.\n");
  printf("       `-._ `-._     .=========.\n");
  printf("           `._ /`-..-          .\n");
  printf("              `-._             .\n");
  printf("                  `-.._______.'\n");
  printf("\n");
  printf("Ceci n'est pas une flag.\n");
  unlink(argv[0]);
  return 0;
}
