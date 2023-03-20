#Import
import numpy as np
import random
from sys import exit

#Notes:
#

#TO DO
#Probably nest up the if statements in gen_masks
#only have to do it once or twice, so not critical for speed, but probably good to do

#Any speed increase on the loop is ideal. Over 1e6 loops and we end up going pretty slow.


#Function Definitions
#-------------------------------------------------------------------
#Makes a random word of length sz_deck, with n_cards set to 1
def gen_hands(n_cards,sz_deck):
    hand = 0
    for i in range(n_cards):
        bit = random.randint(0, sz_deck+1)
        hand |= 1 << bit
    return hand

#Makes masks for bricks
def gen_masks(n_bricks ,n_pairs , n_triples , n_tthirds):
    #For doubles and triples, need to add zero padding
    if n_pairs > 0:
        mask2 = 3
        for i in range(1,n_pairs):
            mask2 = mask2 + (3 << 3*i)
    else:
        mask2 = 0

    if n_triples > 0:    
        mask3 = 7
        for i in range(1,n_triples):
            mask3 = mask3 + (7 << 4*i)
        if n_pairs > 0:
            mask3 = mask3 << 3*n_pairs - 1
    else:
        mask3 = 0

    if n_tthirds > 0:     
        mask32 = 7
        for i in range(1,n_tthirds):
            mask32 = mask32 + (7 << 4*i)
        if n_pairs > 0:
            mask32 = mask32 << 3*n_pairs - 2
        if n_triples > 0:
            mask32 = mask32 << 4*n_triples - 1
    else:
        mask32=0

    #Ideally, make this fill the gaps in the zero padding to generalize to higher numbers of brick cards
    if n_bricks > 0:
        mask1 = (2**(n_bricks)-1)
        if n_pairs > 0:
            mask1 = mask1 << 3*n_pairs - 2
        if n_triples > 0:
            mask1 = mask1 << 4*n_triples - 1
        if n_tthirds > 0:
            mask1 = mask1 << 3*n_pairs - 2
    else:
        mask1 = 0

    return mask1, mask2, mask3, mask32

#Does probability and makes an array of bricks for a trial
def test_brick(hand, mask1, mask2, mask3, mask32):
    a = np.zeros(4)
    #Check singles
    if hand & mask1 > 0:
        a[0] = 1

    #Check pairs
    x = hand & mask2
    if x & x<<1:
        a[1]=1

    #Check Triples
    x = hand & mask3
    if (x & (x << 1)) & (x & (x >> 1)):
        a[2]=1
    
    #Check Tthirds
    x = hand & mask32
    if (x & (x << 1)) | (x & (x >> 1)):
        a[3]=1

    return a


#Main Body
#---------------------------------------------
n_cards = 6
sz_deck = 40

n_iter = 1000000

n_bricks = 1
n_pairs = 1
n_triples = 1
n_tthirds = 1

#Check to see we havent overcommitted the deck
total_bricks = n_bricks + 2*n_pairs + 3*(n_triples+n_tthirds)
if  total_bricks >= 0.75*sz_deck:
    print('Too many bricks!')
    exit()

#Generate Masks, arrays
mask1, mask2, mask3, mask32 = gen_masks(n_bricks, n_pairs, n_triples, n_tthirds)
brick_arr = np.zeros(5)

#Do sims
for ii in range(n_iter+1):

    x = gen_hands(n_cards,sz_deck)
    a = test_brick(x, mask1, mask2, mask3, mask32)

    #For some reason, python uses the max index as exclusive...
    brick_arr[0:4] += a

    if a.any() > 0:
        brick_arr[4] += 1

out_arr = brick_arr.astype('float64') / n_iter

#Output results
print(brick_arr)
print('Brick Rate from Singles: ' + str(out_arr[0]))
print('Brick Rate from Doubles: ' + str(out_arr[1]))
print('Brick Rate from Triples: ' + str(out_arr[2]))
print('Brick Rate from Two Thirds: ' + str(out_arr[3]))
print('Overall Brick Rate: ' + str(out_arr[4]))