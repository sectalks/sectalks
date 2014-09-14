#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int
main(int argc, char **argv)
{
	char buf[3] = {0};
	int c, bi = 0;

	while((c=getc(stdin)) != EOF) {
		if(isxdigit(c)) {
			buf[bi++] = c;
			if(bi == 2) {
				putc(strtol(buf, NULL, 16), stdout);
				bi = 0;
			}
		} else if(bi != 0) {
			fprintf(stderr, "partial hex near '%02x %02x'\n", buf[0], c);
			exit(1);
		} else if(isspace(c)) {
			continue;
		} else {
			fprintf(stderr, "illegal character: %02x\n", c);
			exit(1);
		}
	}
	if(bi != 0) {
		fprintf(stderr, "partial hex near '%02x %02x'\n", buf[0], c);
		exit(1);
	}
	exit(0);
}
