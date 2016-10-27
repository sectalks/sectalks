#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>

int main(int argc, char *argv[]){
    char *infname, *outfname, byte;
    int shift;
    FILE *infile, *outfile;
    char *execargv[2], *execenvp[1];
    if (argc != 2) {
        printf("usage: %s <binary>\n", argv[0]);
        exit(0);
    }
    infname = argv[1];
    outfname = tempnam(NULL, NULL);
    shift = -3;
    infile = fopen(infname, "r");
    outfile = fopen(outfname, "w");
    while(fread(&byte, 1, 1, infile)) {
        byte = (byte + shift) % 256;
        fwrite(&byte, 1, 1, outfile);
    }
    fclose(infile);
    fclose(outfile);
    chmod(outfname, 0755);
    execargv[0] = outfname;
    execargv[1] = NULL;
    execenvp[0] = NULL;
    return execve(outfname, execargv, execenvp);
}
