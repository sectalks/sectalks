#include <stdio.h>
#include <errno.h>
#include <string.h>

/*
 * sc_patch.c
 * 0x01
 * s3my0n
 * supercomputer patcher for sectalk MiniCTF 0x01.
 * december 2013
 */

int main(int argc, char *argv[])
{
    if (argc < 2) {
        printf("Usage: %s <supercomputer>\n", argv[0]);
        return 1;
    }

    FILE *fp = fopen(argv[1], "r+b");
    if (fp == NULL) {
        fprintf(stderr, "%s\n", strerror(errno));
        return 1;
    }

    // make sleep() just ret
    fseek(fp, 0x570, SEEK_SET);
    fwrite("\x90\x90\x90\x90\x90\xc3", 6, 1, fp);

    // 'mv r13, -1' -> 'mv r13, 0'
    fseek(fp, 0xad2, SEEK_SET);
    fwrite("\x49\xc7\xc4\x00\x00\x00\x00", 7, 1, fp);

    fclose(fp);

    return 0;
}
