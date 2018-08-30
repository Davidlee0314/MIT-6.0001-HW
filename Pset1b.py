
# coding: utf-8

# In[ ]:

# %load ps1b
###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1

from collections import Counter

def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    eggs = {}
    avail_weight = target_weight
    
    if target_weight == 0:
        return 0
    elif str(target_weight) in memo:
        return memo[str(target_weight)]
    else:
        if target_weight < egg_weights[-1]:
            avail_eggs = [k for k in egg_weights if k <= target_weight]
            try:
                eggs[str(avail_eggs[-1])] += 1
            except KeyError:
                eggs[str(avail_eggs[-1])] = 1
           
        else:
            avail_eggs = egg_weights
            
            try:
                eggs[str(avail_eggs[-1])] += 1
            except KeyError:
                eggs[str(avail_eggs[-1])] = 1

        memo[str(avail_weight)] = eggs
        avail_weight -= avail_eggs[-1]
    
        if avail_weight < egg_weights[0]:
            return eggs
        else:
            A = dp_make_weight(avail_eggs, avail_weight, memo)
            B = {x: eggs.get(x,0) + A.get(x,0) for x in set(eggs).union(A)}
            return B

    
    
# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 20)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", sum(dp_make_weight(egg_weights, n).values()))
    print()

