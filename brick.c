#include <brick.h>
#include <stats.h>

int main(void){

    //Generate masks
    gen_masks(n_singles, n_pairs, n_triples, n_tthirds,
                &mask1, &mask2, &mask3, &mask32);

    //Check to see we havent overcommitted the deck with bricks
    if (mask1 > (1ULL << (sz_deck-1))){
        printf("Too many bricks!\n");
        exit(EXIT_SUCCESS);
    }
    
    //Initialize other variables
    ll hand;
    int i;
    int ones = 0;
    int twos = 0;
    int threes = 0;
    int tthirds = 0;
    int any = 0;
    
    time_t t;

    srand((unsigned) time(&t));              //Initialize random numbers for gen_hands

    //Loop over iterations
    for(i=0;i<n_iter;i++){

        //Generate a hand
        hand = gen_hand(n_cards,sz_deck);

        //Test if/how the hand bricked
        test_brick(hand, mask1, mask2, mask3, mask32, 
                    &ones, &twos, &threes, &tthirds, &any);
    }
    
    t = clock() - t;
    
    printf("Brick Rate for Singles: %f %%\n",100.*ones/n_iter);
    printf("Brick Rate for Pairs: %f %%\n",100.*twos/n_iter);
    printf("Brick Rate for Triples: %f %%\n",100.*threes/n_iter);
    printf("Brick Rate for Two/Triples: %f %%\n",100.*tthirds/n_iter);
    printf("Overall Brick Rate: %f %%\n",100.*any/n_iter);
    printf("Expected error: %f %%\n",100.*check_error(any,n_iter));

    return 0;
}