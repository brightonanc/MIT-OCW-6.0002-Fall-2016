###########################
# 6.0002 Problem Set 1a: Space Cows
# Name: Brighton Ancelin
# Collaborators:
# Time:
#
# SEARCH FOR "MY_CODE" COMMENT TO FIND MY CONTRIBUTIONS

from ps1_partition import get_partitions
from timeit import default_timer

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # MY_CODE
    cow_dict = {}
    with open(filename, 'r') as f:
        for line in f:
            name, weight = line.split(',')
            cow_dict[name] = int(weight)
    return cow_dict


# Problem 2
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # MY_CODE
    remaining = sorted(cows.copy(), key=cows.get, reverse=True)
    assert cows[remaining[0]] <= limit, "Problem shouldn't be impossible!"
    boarding_list = []
    while remaining:
        cur_list = []
        occupancy = 0
        for cow in remaining:
            if occupancy + cows[cow] <= limit:
                cur_list += [cow]
                occupancy += cows[cow]
            elif occupancy + cows[remaining[-1]] > limit:
                break
        for elem in cur_list:
            remaining.remove(elem)
        boarding_list += [cur_list]
    return boarding_list


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # MY_CODE
    for partition in get_partitions(cows.keys()):
        valid_partition = True  # Innocent until proven guilty
        for trip in partition:
            weight_total = sum(cows[x] for x in trip)
            if weight_total > limit:
                valid_partition = False
                break
        if valid_partition:
            return partition
    assert False, "Problem shouldn't be impossible!"


# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # MY_CODE
    cows = load_cows('ps1_cow_data.txt')
    start = default_timer()
    sol_greedy = greedy_cow_transport(cows)
    end = default_timer()
    time_greedy = end - start
    start = default_timer()
    sol_brute = brute_force_cow_transport(cows)
    end = default_timer()
    time_brute = end - start
    print('Greedy:', sol_greedy)
    print('    Length:', len(sol_greedy))
    print('    Time:', time_greedy)
    print('Brute:', sol_brute)
    print('    Length:', len(sol_brute))
    print('    Time:', time_brute)
    print('Time for greedy was {0}x faster than brute'.format(
            time_brute/time_greedy))

# MY_CODE
if __name__ == '__main__':
    compare_cow_transport_algorithms()
