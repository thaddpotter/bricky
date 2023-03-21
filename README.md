# bricky
Originally made this to calculate the brick odds for specific card combinations in Yugioh

Want to extend this further to calculate general consistency. Odds of a great hand, good hand, and bad hand given some list of input parameters.
Potentially even wrap the input in a gui to make it easier to use.

Immediate TODO:
Speeding up gen_hands and check bricks if possible. Lost some speed after fixing a mistake in gen_hands which resulted in some cards able to be picked twice in hands. Not super slow, but still a bit annoying to run for 10 sec every time. Use numba?
Also, error estimation on the percentages would be good. Added a basic one that I found online, stdev/root(N), but doesnt line up with repeatability I see. Theres probably some method that monte carlo sims use.
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3337209/

