#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <signal.h>
#include <unistd.h>

#define FLAG_FILE "./flag.txt"
#define MAX_NAME_LEN 100
#define TRUE 1
#define FALSE 0
#define USER_CIA_CTF 1002
#define USER_CIA 1003

/* 
 * Sectalks CTF Challenge 
 * Antivirus Hash Checker
 *
 * by paste_bin 9/3/2017
 *
 */


int ciaVerified(char *str);
int verify_prog(char *hash_bytes);

int main(int argc, char *argv[]){
	setreuid(USER_CIA_CTF,0);
	printf("~~Central Inteligence AntiVirus~~\n");
	printf("Simply enter the name of"
		" the program you think could"
		" be malware and I'll tell you"
		" using my cyber magic");

	char buff[1000];
	int counter = 0;
	printf("Enter the name of the program"
		" you suspect to be malware\n");
	printf("PROG_NAME:");
	fflush(stdout);
	memset(buff, 0, 1000);
	scanf("%s", buff);

	for (counter = 0; counter < 1000; counter++){
		if (!isalnum(buff[counter]) && buff[counter]){
			printf("%c\n", buff[counter]);
			buff[buff[counter]] = 'A'^buff[counter+1];
		}
	}
	verify_prog(buff);
	// fflush(stdout);
}

static void handler(int sig, siginfo_t *dont_care, void *dont_care_either) {
	printf("Yep, that's malware\n");
	// fflush(stdout);
	exit(0);
}

int ciaVerified(char *str){
	setreuid(USER_CIA,0);
	// printf("STR: '%s'\n", str);
	char cmd[MAX_NAME_LEN] = "./ciaMalware.sh ";
	strcat(cmd, str);
	strcat(cmd, " ");
	strcat(cmd, FLAG_FILE);
	// printf("CMD: %s\n", cmd);

	FILE *cia = popen(cmd, "r");
	char buf[256];
	int ciaVerified = FALSE;
	if (fgets(buf, sizeof(buf), cia) != 0) {
	    ciaVerified = TRUE;
	}
	// printf("FLAG: %s\n", buf);
	pclose(cia);
	setreuid(USER_CIA_CTF,0);
	return ciaVerified;
}

int verify_prog(char *hash_bytes){
	char buf[1000];
	char hash[32];
	int i = 0;
	struct sigaction sa;

	memset(&sa, 0, sizeof(sigaction));
	sigemptyset(&sa.sa_mask);

	sa.sa_flags     = SA_NODEFER;
	sa.sa_sigaction = handler;

	sigaction(SIGSEGV, &sa, NULL); /* ignore whether it works or not */ 
	int hash_len_half = strlen(hash_bytes)/2;
	// printf("len %d\n", hash_len_half);
	for (i = 0; i < hash_len_half; i++){
		buf[i] = hash_bytes[hash_len_half+i]^hash_bytes[i];
	}
	memcpy(hash, buf, hash_len_half);
	// printf("HASH %s\n", hash);
	if (ciaVerified(hash)){
		printf("This software is legit\n"
			"Here is its signature: ");
		printf(hash);
	}else{
		printf("This software is crap\n"
			"Here is its signature: ");
		printf(hash);
	}

	// fflush(stdout);

}
