#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
  printf("This is a sample QXR executable.\n");
  printf("     (_)\n");
  printf("    <___>\n");
  printf("     | |___________________________________________\n");
  printf("     | |`-._`-._         :|    |:         _.-'_.-'|\n");
  printf("     | |`-._`-._`-._     :|    |:     _.-'_.-'_.-'|\n");
  printf("     | |    `-._`-._`-._ :|    |: _.-'_.-'_.-'    |\n");
  printf("     | | _ _ _ _`-._`-._`:|    |:`_.-'_.-' _ _ _ _|\n");
  printf("     | |------------------      ------------------|\n");
  printf("     | |                                          |\n");
  printf("     | |__________________      __________________|\n");
  printf("     | |- - - - -_.--_.--:|    |:--._--._- - - - -|\n");
  printf("     | |     _.-'_.-'_.-':|    |:`-._`-._`-._     |\n");
  printf("     | | _.-'_.-'_.-'    :|    |:    `-._`-._`-._ |\n");
  printf("     | |'_.-'_.-'        :|    |:        `-._`-._`|\n");
  printf("     | |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");
  printf("     | |\n");
  printf("     | |\n");
  printf("     | |\n");
  printf("     | |\n");
  printf("     | |\n");
  printf("     | |\n");
  printf("\n");
  printf("This is flag 1/2.\n");
  unlink(argv[0]);
  return 0;
}
