#include <stdio.h>
#include <stdlib.h>
#include <math.h>
typedef unsigned long long ll;  //Alias for hand datatype

//Returns number of bits in a value
//This needs to be able to handle up to 64 bit words
int countSetBits(ll n)
{
    unsigned int count = 0;
    while (n) {
        count += n & 1;
        n >>= 1;
    }
    return count;
}

//Makes a ull with n_cards random bits set to 1
//With a max 60 card deck, a 64 bit can cover everything, and the last digits just wont be used
ll  gen_hand(int n_cards, int sz_deck){
    
    ll hand = 0;                    //Output
    
    while(countSetBits(hand) < n_cards){
        int shift = rand() % (sz_deck-1);    // Bit position between 0 and n_cards-1
        hand |= (1ULL << shift);
    }

    return hand;
}

//Tests a hand for bricks
void test_brick(ll hand, ll mask1, ll mask2, ll mask3, ll mask32,
                int *ones, int *twos, int *threes, int *tthirds, int *any){

    ll x;
    int j = 0;

    //Check Singles
    if ((hand & mask1) > 0){
        ++(*ones);
        j = 1;
    }

    //Check Doubles
    x = hand & mask2;
    if ((x & (x << 1)) > 0){
        ++(*twos);
        j = 1;
    }

    //Check Triples
    x = hand & mask3;
    if ((x & (x << 1)) & (x & (x >> 1))){
        ++(*threes);
        j = 1;
    }

    //Check Twothirds
    x = hand & mask32;
    if (((x & (x << 1)) > 0) | ((x & (x << 1)) > 0)){
        ++(*tthirds);
        j = 1;
    }

    //Overall Brick rate
    if(j>0){
        ++(*any);
    }

//No return, but brick counts have been modified
}

//Makes a set of masks given a certain number of brick types
void gen_masks(int n_singles, int n_pairs, int n_triples, int n_tthirds,
                ll *mask1, ll *mask2, ll *mask3, ll *mask32){
    
    int i;

    //Refresh masks to zero
    *mask1 = 0;
    *mask2 = 0;
    *mask3 = 0;
    *mask32 = 0;

    //To avoid adjacent brick pairs, need to zero pad between sets
    //Pair masks
    if (n_pairs > 0){
        for(i=0; i < n_pairs; i++){
            *mask2 += (3ULL << 3*i);
        }
    }

    //Triple Masks
    if (n_triples > 0){
        for(i=0; i < n_triples; i++){
            *mask3 += (7ULL << 4*i);
        }
        //Bitshift to avoid overlap with prev masks
        if (n_pairs > 0){
            *mask3 <<= (3*n_pairs-2);
        }
    }

    //Twothirds masks
    if (n_tthirds > 0){
        for(i=0; i < n_tthirds; i++){
            *mask32 += (7ULL << 4*i);
        }
        //Bitshift to avoid overlap with prev masks
        if (n_pairs > 0){
            *mask32 <<= (3*n_pairs-2);
        }
        if (n_triples > 0){
            *mask32 <<= (4*n_triples-1);
        }
    }

    //Singles masks
    if (n_singles > 0){
        *mask1 = (1ULL << n_singles)-1;
        if (n_pairs > 0){
            *mask1 <<= (3*n_pairs-2);
        }
        if (n_triples > 0){
            *mask1 <<= (4*n_triples-1);
        }
        if (n_pairs > 0){
            *mask1 <<= (3*n_pairs-2);
        }
        if (n_triples > 0){
            *mask1 <<= (4*n_triples-1);
        }
    }
    //No return, but masks have been modified
}

//Basic error estimator for calculated probabilities
float check_error(int any, int n_iter){
    double err;
    err = sqrt((n_iter - any) * (pow(any,2) / n_iter + any) / n_iter);
    return err/n_iter;
}
    