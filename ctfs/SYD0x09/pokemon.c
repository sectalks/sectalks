#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

void playGame();
struct pokemon* getEnemyPokemon();
struct pokemon* buildPlayerTeam();
struct pokemon getWaterPokemon();
struct pokemon getFirePokemon();
struct pokemon getGrassPokemon();
void getEnemySaying();
void abc();
char * getEnemyName();
void fight(struct pokemon, struct pokemon);
void password();

int flag_password;
time_t start, stop;

struct pokemon{
  char name[10];
  int attack;
  char element[10];
};

void abc(){
  static int wins = 0;
  static char flag[] = "sdaxtjmbefdv"; 
  flag[wins] = flag[wins] ^ wins;
  wins++;
  printf("You win!\n\n");
  printf("------------------------------\n");
  if(wins < 15){
    playGame();
  }
  password(flag);
  exit(1);
}

void password(char *flag){
  int password;
  printf("Congrats, Enter Password\n");
  fflush(stdout);
  scanf("%6d", &password);
  //flag_password = flag_password + 1;
  if(password == -~flag_password){
    printf("%s\n", flag);
    fflush(stdout);
  }
  else{
    printf("Wrong!\n");
    printf("Correct password: %d\n", flag_password + 1);
  }
}

void playGame(){
  struct pokemon *team;
  struct pokemon *enemy;
  getEnemySaying();

  char *name;
  name = getEnemyName();

  enemy = getEnemyPokemon();
  printf("%s sends out %s [%s.]\n\n", name, enemy[0].name, enemy[0].element);
  fflush(stdout);
  team = buildPlayerTeam();
  printf("Who will you choose?\n");
  printf("[1] %s [%s].\n[2] %s [%s].\n[3] %s [%s].\n", team[0].name, team[0].element, team[1].name, team[1].element, team[2].name, team[2].element);
  fflush(stdout);
  int choice = 0;
  scanf(" %d", &choice);

  struct pokemon player;

  switch(choice){
    case 1 : player = team[0]; break;
    case 2 : player = team[1]; break;
    case 3 : player = team[2]; break;
    default : /* Optional */
       printf("Failed\n");
       exit(1);
  }
  fight(enemy[0], player);
}

void fight(struct pokemon enemy, struct pokemon player){
  stop = time(NULL);
  if(stop-start > 10){
    printf("Times up\n");
    exit(1);
  }
  printf("\n%s [%s] vs %s [%s]\n", enemy.name, enemy.element, player.name, player.element);

 int win = 0;

 if(!(strcmp(player.element, "Fire")) && !(strcmp(enemy.element, "Grass"))){
  abc();
 } else if(!(strcmp(player.element, "Grass")) && !(strcmp(enemy.element, "Water"))){  abc();
 } else if(!(strcmp(player.element, "Water")) && !(strcmp(enemy.element, "Fire"))){
  abc();
 } else{
  printf("You lost\n");
  exit(1);
 }

}

char * getEnemyName(){
  char *name[15];
  srand(time(NULL));
  int counter = rand() % 15;
  name[0] = "Beauty";
  name[1] = "Biker";
  name[2] = "Bird Keeper";
  name[3] = "Blackbelt";
  name[4] = "Bug Catcher";
  name[5] = "Burglar";
  name[6] = "Cooltrainer";
  name[7] = "Cue Ball";
  name[8] = "Engineer";
  name[9] = "Fisherman";
  name[9] = "Gambler";
  name[10] = "Clown";
  name[12] = "Commander";
  name[13] = "Cowgirl";
  name[14] = "Cyclist";
  return(name[counter]);
}


void getEnemySaying(){
  char *talk[15];
  srand(time(NULL));
  int counter = rand() % 15;
  talk[0] = "Pokemon fight? Cool! Rumble!";
  talk[1] = "Come out and play little mouse!";
  talk[2] = "Ah! This mountain air is delicious!";
  talk[3] = "Hey! You're not wearing shorts!";
  talk[4] = "Eek! Did you touch me?";
  talk[5] = "Wait! You'll have a heart attack!";
  talk[6] = "Do you want to Pokemon with me?";
  talk[7] = "I'm not into it, but OK! Let's go!";
  talk[8] = "I'm a rambling, gambling dude!";
  talk[9] = "Hey kid, want to see my Pokemon?";
  talk[10] = "I'd rather be working";
  talk[11] = "I like shorts!";
  talk[12] = "Mostly I breathe fire, but want to exchange numbers?";
  talk[13] = "I’m sure that you will be dazzled by my mentor’s breathtakingly elegant battle style!";
  talk[14] = "This brat’s tough. Tougher than I can put into words, and I know a lot of words!";

  printf("\n%s\n\n", talk[counter]);
  fflush(stdout);
}



struct pokemon* getEnemyPokemon(){

  struct pokemon *enemy = (struct pokemon*)malloc(1*sizeof(struct pokemon));
  srand(time(NULL));
  int type = rand() % 3;
  if(type == 0){
    enemy[0] = getWaterPokemon();
  } else if(type == 1){
    enemy[0] = getFirePokemon();
  } else if(type == 2){
    enemy[0] = getGrassPokemon();
  } else{
    printf("Dafuq?\n");
    exit(1);
  }

  return(enemy); 
}

struct pokemon* buildPlayerTeam(){
  struct pokemon *team=(struct pokemon*)malloc(3*sizeof(struct pokemon));
  team[0] = getWaterPokemon();
  team[1] = getFirePokemon();
  team[2] = getGrassPokemon();
  return(team);
}

struct pokemon getWaterPokemon(){
  srand(time(NULL));
  int n = rand() % 10;

  rand() % 10;
  char *water[10];
  water[0] = "Squirtle";
  water[1] = "Psyduck";
  water[2] = "Horsea";
  water[3] = "Vaporeon";
  water[4] = "Luvdisc";
  water[5] = "Oshawott";
  water[6] = "Swampert";
  water[7] = "Seel";
  water[8] = "Kingler";
  water[9] = "Magikarp";
  struct pokemon pokemon;
  strcpy(pokemon.name, water[n]);
  strcpy(pokemon.element, "Water");
  //printf("[1] %s [%s]\n", pokemon.name, pokemon.element);
  return(pokemon);
}


struct pokemon getFirePokemon(){
  srand(time(NULL));
  int n = rand() % 10;

  rand() % 10;
  char *fire[10];
  fire[0] = "Charmander";
  fire[1] = "Vulpix";
  fire[2] = "Growlithe";
  fire[3] = "Ponyta";
  fire[4] = "Rapidash";
  fire[5] = "Magmar";
  fire[6] = "Flareon";
  fire[7] = "Moltres";
  fire[8] = "Slugma";
  fire[9] = "Ho-oh";
  struct pokemon pokemon;
  strcpy(pokemon.name, fire[n]);
  strcpy(pokemon.element, "Fire");
  //printf("[2] %s [%s]\n", pokemon.name, pokemon.element);
  return(pokemon);
}

struct pokemon getGrassPokemon(){
  srand(time(NULL));
  int n = rand() % 10;

  rand() % 10;
  char *grass[10];
  grass[0] = "Bulbasaur";
  grass[1] = "Chikorita";
  grass[2] = "Meganium";
  grass[3] = "Bellossom";
  grass[4] = "Hoppip";
  grass[5] = "Sunflora";
  grass[6] = "Celebi";
  grass[7] = "Grovyle";
  grass[8] = "Sceptile";
  grass[9] = "Lotad";
  struct pokemon pokemon;
  strcpy(pokemon.name, grass[n]);
  strcpy(pokemon.element, "Grass");
  //printf("[3] %s [%s]\n", pokemon.name, pokemon.element);
  return(pokemon);
}

int main(){
 srand(time(NULL));
 start = time(NULL);
 flag_password = rand() % 999999;
 printf("\nSeed value = %d\n", flag_password);
 fflush(stdout);
 playGame();
 return 0;
}

