#include <stdio.h>
#include <string.h>

int main() {
	char a[] = "XXXXXX"
	int b = strlen(a);
	for (int c = 0; c < b; c++) {
		if (c > 0) a[c] ^= a[c-1];
		a[c] ^= a[c] >> 3;
		a[c] ^= a[c] >> 2;
	  a[c] ^= a[c] >> 1;
		printf("%02x", (unsigned int)(a[c]));
	}
	return 0;
}
