# mybots
COMP_SCI 396, Artificial Life: Ludobots Tasks  

# Assignment 6:

Run search.py to recreate results. Creates are created randomly with between 1 and 20 links, with dimensions between 0.2 and 1 (specified in constants.py). If there is no movement, then you happened to generate a snake where none of the sensor links are touching the ground.

# Assignment 5:

The Fitness metric is a weighted sum of two numbers: 1) the greatest number of consecutive time steps that the robot is in the air, and 2) the sum of all time intervals (above some threshold) in which the robot is in the air.

Only maximizing first value evolves robots that do a single very high jump, but they usually fall over afterwards. Adding in the second metric resulted in robots that jumped multiple times.

These values are calculated during the simulation, and most of this logic happens in the Sense() function in robot.py. At the end of the simulation, I calculate the final Fitness by taking a weighted sum of the two metrics specified above.

To achieve my results, I ran batches with population size of 20 and 100 generations. Each batch stored the weights of the single best resulting robot. I ran 20 of these batches, and then used those 20 robots as the starting population for 500 more generations. However, I only did this to test how far these robots could go, and good results can be obtained by just doing 20x100 or 20x500. Run search.py to try it yourself.