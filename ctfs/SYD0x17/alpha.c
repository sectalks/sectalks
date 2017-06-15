#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

const char secret[] = "Wubba lubba dub dub!";

void run() {
    char buf[32];
    read(0, buf, 4096);
}

int main(int argc, char **argv) {
    setbuf(stdout, NULL);
    printf("secret: %p\n", secret);
    printf("system: %p\n", system);
    run();
    printf("-- goodbye :)\n");
    return 0;
}
