#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>

int main(int argc, char *argv[]){
    char *infname, *outfname, byte;
    int i;
    char mask[4] = { 0x00, 0x11, 0x0D, 0x13 };
    FILE *infile, *outfile;
    char *execargv[2], *execenvp[1];
    if (argc != 2) {
        printf("usage: %s <binary>\n", argv[0]);
        exit(0);
    }
    infname = argv[1];
    outfname = tempnam(NULL, NULL);
    infile = fopen(infname, "r");
    outfile = fopen(outfname, "w");
    i = 0;
    while(fread(&byte, 1, 1, infile)) {
        byte ^= mask[i];
        fwrite(&byte, 1, 1, outfile);
        i = (i + 1) % 4;
    }
    fclose(infile);
    fclose(outfile);
    chmod(outfname, 0755);
    execargv[0] = outfname;
    execargv[1] = NULL;
    execenvp[0] = NULL;
    return execve(outfname, execargv, execenvp);
}
