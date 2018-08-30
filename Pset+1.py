
# coding: utf-8

# In[ ]:

# %load ps1a
###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: David
# Collaborators: None
# Time:

from ps1_partition import get_partitions
import time
import re

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
    file = open(filename,"r")
    cow_dict = {}
    file_read = file.read()
    weight = re.findall(r'\d{1,2}', file_read)
    name = re.findall(r'[A-Z][a-z]+\s[A-Z][a-z]+\-[a-z]+|[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+', file_read)
    for index, w in enumerate(name):
        cow_dict[w] = int(weight[index])
    return cow_dict


# Problem 2
def greedy_cow_transport(cows,limit=10):
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
    trip_list = []
    cows_avail = sorted(cows, key = cows.get, reverse = True)
    
    while len(cows_avail) != 0:
        totalweight = 0
        trip = []
        index_l = []
        
        for index, cow in enumerate(cows_avail):
            if (cows[cow] + totalweight) <= limit:
                totalweight += cows[cow]
                trip.append(cow)
                index_l.append(index)
                
        cows_avail = [cow for i, cow in enumerate(cows_avail) if i not in index_l]
        trip_list.append(trip)

    return trip_list

# Problem 3
def brute_force_cow_transport(cows,limit = 10):
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
    trip_list = []
    cows_avail = sorted(cows, key = cows.get, reverse = True)
    cow_list = get_partitions(cows_avail)
    poss = []
            
    for partition in cow_list:
        overload = False
        
        for trip in partition:
            totalweight = 0
            
            for cow in trip:
                totalweight += cows[cow]
                
                if totalweight > limit:
                    overload = True
                    
        if not overload:
            poss.append(partition)
                   
    return min(poss, key =len)      

      
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
    cow_dict = load_cows("ps1_cow_data_2.txt")

    start = time.time()
    greedy_trip = greedy_cow_transport(cow_dict)
    end = time.time()
    print(end-start)
    #print("Greedy algorithm takes",(end-time),"seconds.")
    print("Trips:",greedy_trip,"It needs",len(greedy_trip),"trips.")
    
    start = time.time()
    brute_trip = brute_force_cow_transport(cow_dict)
    end = time.time()
    print(end-start)
    #print("Brute Force algorithm takes",(end-time),"seconds.")
    print("Trips:",brute_trip,"\nIt needs",len(brute_trip),"trips.")
    
if __name__ == "__main__":
    compare_cow_transport_algorithms()

