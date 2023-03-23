# Makes masks for bricks
def gen_masks():

    n_bricks = 1
    n_pairs = 1
    n_triples = 1
    n_tthirds = 1

    # For doubles and triples, need to add zero padding
    if n_pairs > 0:
        mask2 = 3
        for i in range(1, n_pairs):
            mask2 = mask2 + (3 << 3*i)
    else:
        mask2 = 0

    if n_triples > 0:
        mask3 = 7
        for i in range(1, n_triples):
            mask3 = mask3 + (7 << 4*i)
        if n_pairs > 0:
            mask3 = mask3 << 3*n_pairs - 1
    else:
        mask3 = 0

    if n_tthirds > 0:
        mask32 = 7
        for i in range(1, n_tthirds):
            mask32 = mask32 + (7 << 4*i)
        if n_pairs > 0:
            mask32 = mask32 << 3*n_pairs - 2
        if n_triples > 0:
            mask32 = mask32 << 4*n_triples - 1
    else:
        mask32 = 0

    # Ideally, make this fill the gaps in the zero padding to generalize to higher numbers of brick cards
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