# Import
from sys import exit

import numpy as np
from make_deck import gen_masks
from numpy.random import PCG64, Generator

rng = Generator(PCG64())

# Notes:
#

# TO DO
# Probably nest up the if statements in gen_masks
# only have to do it once or twice, so not critical for speed, but probably good to do
# Would also be good to add something to start interfacing with an actual decklist, or allow read in from a table.
# Any speed increase on the loop is ideal. Over 1e6 loops and we end up going pretty slow.


# Function Definitions
# -------------------------------------------------------------------
# Makes a random word of length sz_deck, with n_cards set to 1
def gen_hands(n_cards, sz_deck):
    hand = 0
    inds = rng.choice(sz_deck, size=n_cards, replace=False, shuffle=False)
    for i in range(n_cards):
        hand |= 1 << inds[i]
    return hand

# Does probability and makes an array of bricks for a trial
def test_brick(hand, mask1, mask2, mask3, mask32):
    a = np.zeros(4)
    # Check singles
    if hand & mask1 > 0:
        a[0] = 1

    # Check pairs
    x = hand & mask2
    if x & x << 1:
        a[1] = 1

    # Check Triples
    x = hand & mask3
    if (x & (x << 1)) & (x & (x >> 1)):
        a[2] = 1

    # Check Tthirds
    x = hand & mask32
    if (x & (x << 1)) | (x & (x >> 1)):
        a[3] = 1

    return a

#Basic error estimator for calculated probabilities
def check_error(arr, n_iter):
    counts = arr.astype(np.float64)
    error = np.sqrt((n_iter - counts) * (counts**2 / n_iter + counts) / n_iter)
    return error/n_iter


# Main Body
# ---------------------------------------------
n_cards = 6
sz_deck = 40

n_iter = 1000000

n_bricks = 1
n_pairs = 1
n_triples = 1
n_tthirds = 1

# Generate Masks, arrays
mask1, mask2, mask3, mask32 = gen_masks()

# Check to see we havent overcommitted the deck
if (mask1 + mask2 + mask3 + mask32) > (1 << (sz_deck-1)):
    print('Too many bricks!')
    exit()

# Do sims
brick_arr = np.zeros(5)
for ii in range(n_iter+1):

    x = gen_hands(n_cards, sz_deck)
    a = test_brick(x, mask1, mask2, mask3, mask32)

    # For some reason, python uses the max index as exclusive...
    brick_arr[0:4] += a

    if a.any() > 0:
        brick_arr[4] += 1

out_arr = 100 * brick_arr.astype('float64') / n_iter
error = 100 * check_error(brick_arr, n_iter)

# Output results
print('Brick Rate from Singles: ' + str(out_arr[0]))
print('Brick Rate from Doubles: ' + str(out_arr[1]))
print('Brick Rate from Triples: ' + str(out_arr[2]))
print('Brick Rate from Two Thirds: ' + str(out_arr[3]))
print('Overall Brick Rate: ' + str(out_arr[4]))
print(error)