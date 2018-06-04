###########################
# 6.0002 Problem Set 1b: Space Change
# Name: Brighton Ancelin
# Collaborators:
# Time:
# Author: charz, cdenise
# SEARCH FOR "MY_CODE" COMMENT TO FIND MY CONTRIBUTIONS

#================================
# Part B: Golden Eggs
#================================

from timeit import default_timer


# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}, use_Memo=True,
                   use_Ones_Optimizaton=True):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.

    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)

    Returns: int, smallest number of eggs needed to make target weight
    """
    # MY_CODE
    def call_dp(egg_weights, target_weight):

        # Further optimization, provided we always anticipate a value of 1
        # to be in the tuple
        if use_Ones_Optimizaton and egg_weights == (1):
            return target_weight

        if use_Memo:
            key = (egg_weights, target_weight)
            if key in memo:
                return memo[key]
            else:
                val = dp_make_weight(egg_weights, target_weight, memo,
                                     use_Memo, use_Ones_Optimizaton)
                memo[key] = val
                return val
        else:
            return dp_make_weight(egg_weights, target_weight, memo,
                                  use_Memo, use_Ones_Optimizaton)
    if 0 == target_weight:
        return 0
    if target_weight < egg_weights[-1]:
        return call_dp(egg_weights[:-1], target_weight)
    # First, deal with reality where max weight is taken (take reality = tr)
    tr_egg_count = call_dp(egg_weights, target_weight - egg_weights[-1])
    tr_egg_count += 1
    # Then, deal with reality where max weight is left (leaving reality = lr)
    if 1 < len(egg_weights):
        lr_egg_count = call_dp(egg_weights[:-1], target_weight)
        if tr_egg_count < lr_egg_count:
            return tr_egg_count
        else:
            return lr_egg_count
    return tr_egg_count



# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    # MY_CODE
    # As the above comment invited, I added more.
    for egg_weights in [(1, 5, 10, 25), (1,10,100,1000),(1,2,5,10,20,25,30,50),
                        (1,2,3,4,5,6,7,8,9), (1, 19, 20, 30, 60)]:
        n = 99
        print("Egg weights =", egg_weights)
        print("n =", n)
        start_none = default_timer()
        res_none = dp_make_weight(egg_weights, n, use_Memo=False,
                                  use_Ones_Optimizaton=False)
        end_none = default_timer()
        time_none = end_none - start_none
        start_memo = default_timer()
        res_memo = dp_make_weight(egg_weights, n, use_Memo=True,
                                  use_Ones_Optimizaton=False)
        end_memo = default_timer()
        time_memo = end_memo - start_memo
        start_ones = default_timer()
        res_ones = dp_make_weight(egg_weights, n, use_Memo=False,
                                  use_Ones_Optimizaton=True)
        end_ones = default_timer()
        time_ones = end_ones - start_ones
        start_memoones = default_timer()
        res_memoones = dp_make_weight(egg_weights, n, use_Memo=True,
                                      use_Ones_Optimizaton=True)
        end_memoones = default_timer()
        time_memoones = end_memoones - start_memoones
        assert res_none == res_memo == res_ones == res_memoones, 'Not equal'
        print("Actual output:", res_none)
        print("Time incr for memo:", time_none/time_memo)
        print("Time incr for ones:", time_none/time_ones)
        print("Time incr for memoones:", time_none/time_memoones)
        print("Time none-ones:", time_none - time_ones)
        print("Time memo-memoones:", time_memo - time_memoones)

        print()
