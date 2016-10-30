#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]){
    char *infname, *outfname, byte;
    int shift;
    FILE *infile, *outfile;
    if (argc != 4) {
        printf("usage: %s <infile> <outfile> <shift>\n", argv[0]);
        exit(0);
    }
    infname = argv[1];
    outfname = argv[2];
    shift = atoi(argv[3]);
    printf("in: %s, out: %s, shift: %d\n", infname, outfname, shift);
    infile = fopen(infname, "r");
    outfile = fopen(outfname, "w");
    while(fread(&byte, 1, 1, infile)) {
        byte = (byte + shift) % 256;
        fwrite(&byte, 1, 1, outfile);
    }
    return 0;
}
