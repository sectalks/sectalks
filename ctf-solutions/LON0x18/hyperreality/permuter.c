#include <openssl/sha.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char *charset =
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
char buffer[16] = {0};
int buffer_len = 15;
int suffix_len = 5;
unsigned char wanted_end[3] = {0};
unsigned char hash[SHA_DIGEST_LENGTH];

void printHash(unsigned char *hash) {
  if (hash == NULL) {
    printf("null hash\n");
    exit(-1);
  }

  for (int i = 0; i < SHA_DIGEST_LENGTH; i++) {
    printf("%02x", hash[i]);
  }
  printf("\n");
}

int has_end(unsigned char *hash) {
  if (hash == NULL) {
    printf("null hash\n");
    exit(-1);
  }

  if (hash[17] == wanted_end[0] && hash[18] == wanted_end[1] && hash[19] == wanted_end[2])
    return 0;

  return 1;
}

void permute(int level) {
  const char *charset_ptr = charset;
  if (level == 0) {
    /* printf("%s ", buffer); */
    SHA1(buffer, buffer_len, hash);
    /* printHash(hash); */
    if (has_end(hash) == 0) {
      printf("%s ", buffer);
      /* printHash(hash); */
      exit(0);
    }

  } else {
    while (buffer[buffer_len - suffix_len + level - 1] = *charset_ptr++) {
      permute(level - 1);
    }
  }
}

int main(int argc, char **argv) {
  strcpy(buffer, argv[1]); // copy prefix

  // convert hex string to unsigned char for comparison with hash
  char temp[3] = {0};
  for (int i = 0; i < strlen(argv[2]) - 1; i += 2) {
    temp[0] = argv[2][i];
    temp[1] = argv[2][i + 1];
    wanted_end[i / 2] = (unsigned char)strtol(temp, NULL, 16);
  }

  permute(suffix_len);
  return 0;
}
