#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]){
    char *infname, *outfname, byte;
    int i;
    char mask[4] = { 0x00, 0x11, 0x0D, 0x13 };
    FILE *infile, *outfile;
    if (argc != 3) {
        printf("usage: %s <infile> <outfile>\n", argv[0]);
        exit(0);
    }
    infname = argv[1];
    outfname = argv[2];
    infile = fopen(infname, "r");
    outfile = fopen(outfname, "w");
    i = 0;
    while(fread(&byte, 1, 1, infile)) {
        byte ^= mask[i];
        fwrite(&byte, 1, 1, outfile);
        i = (i + 1) % 4;
    }
    return 0;
}
