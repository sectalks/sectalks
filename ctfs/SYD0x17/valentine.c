#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>

char * banner;
char * rose = ""
"            .   .    .  . .\n"
"             )   \\  (  ( /\n"
"            / '   )  )  \\\n"
"           (   './  / ._.)\n"
"            \\    '.-.'  \\\n"
"            (\\ /'      _)\n"
"             '(   . -_.'\n"
"                | | |\\\n"
"                 ||| --------.\n"
"            _____|||_____     '.\n"
"          /              \\     |\n"
"         |                |    |\n"
"          \\   ___________/   ._|\n"
"          /               \\ /  '\n"
"         |                 |--'\n"
"          \\   ____________/\n"
"          /              \\\n"
"         |                |\n"
"          \\   ___________/\n"
"          /            \\\n"
"         |              |\n"
"          \\ ___________/\n"
"                 |||\n"
"                 |||\n"
"                 ||\n"
"                 |\n";

void set_banner(const char * s) {
    int prot = PROT_READ | PROT_WRITE | PROT_EXEC;
    mprotect((char*)((size_t)banner & 0x1000), 4096, prot);
    banner = (char*)s;
}

void give_rose() {
    printf("%s\n", rose);
}

int main(int argc, char **argv) {
    setbuf(stdout, NULL);
    set_banner("\n"
            "                 .-\"\"\"-.    .-\"\"\"-.\n"
            "                /       `..'       \\\n"
            "               |                    |\n"
            "               |      H A P P Y     |\n"
            "                \\    VALENTINE'S   /\n"
            "               __\\     D A Y !    /\n"
            "          _   /  |`\\            /'\n"
            "         | \\  \\/_/  `\\        /'\n"
            "         \\_\\| / __    `\\    /'\n"
            "            \\/_/__\\     `\\/'  .--='/~\\\n"
            "     ____,__/__,_____,______)/   \/{~}}}\n"
            "     -,-----,--\\--,-----,---,\\'-' {{~}}\n"
            "             __/\\_            '--=.\\}/\n"
            "            /_/ |\\\\\n"
            "                 \\/");

    char note[4096];
    char gift[1024];
    char buf[8];
    memset(buf, 0, sizeof(buf));
    memset(gift, 0, sizeof(gift));
    memset(note, 0, sizeof(note));

    printf(banner);

    printf("\nHow many roses would you like for Valentine's Day?: ");
    fgets(buf, sizeof(buf), stdin);
    buf[strlen(buf)-1] = '\0';
    int count = atoi(buf);

    char str[256];
    sprintf(str, "Prepare yourself for %s secret admirer(s)!\n", buf);
    printf(str);

    printf("\nIs there a limit to your love?: ");
    fgets(buf, sizeof(buf), stdin);
    buf[strlen(buf)-1] = '\0';
    int limit = atoi(buf);

    if (limit > 1024 || limit == 0) {
	    limit = 1024;
    }

    printf("\nWhat would you like written on the notes?:\n");
    fgets(note, sizeof(note), stdin);
    memcpy(gift, note, limit);

    for (int i = 1; i <= count; i++) {
	    printf("\n+----->  You got a rose! That makes %d :)\n", i);
	    printf("+----->  %s\n", gift);
	    give_rose();
	    sleep(1);
    }

    return 0;
}
