#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

//Types and definitions
typedef unsigned long long ll;  //Alias for hand datatype

int sz_deck = 40;
int n_iter = 1000000;
int n_cards = 5;

int n_singles = 1;
int n_pairs = 1;
int n_triples = 1;
int n_tthirds = 1;

ll mask1;
ll mask2;
ll mask3;
ll mask32;

//Functions
int countSetBits(ll n);
ll  gen_hand(int n_cards, int sz_deck);
void test_brick(ll hand, ll mask1, ll mask2, ll mask3, ll mask32,
                int *ones, int *twos, int *threes, int *tthirds, int *any);
void gen_masks(int n_singles, int n_pairs, int n_triples, int n_tthirds,
                ll *mask1, ll *mask2, ll *mask3, ll *mask32);
float check_error(int any, int n_iter);
