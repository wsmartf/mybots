# mybots
COMP_SCI 396, Artificial Life: Ludobots Tasks  

# Assignment 7:

Run search.py to recreate results. Bodies are randomly generated with 2-7 links. Links are generated one-by-one, and each new link is randomly placed on one of the 5 open faces of the previous one. The shape of each link is determined by assigning random values between 0.2 and 1.5 to each dimension of the rectangle. The joint axes are also randomly assigned, and each joint has 80% freedom of movement, which allows for a wide variety of movement. Theoretically, the body can fill up all of 3D space, as the path of generated links can randomly travel in any direction. 

As the body is constructed, the name of each "sensing" link is stored. To generate the brain, I iterate through these links and make a connection between each sensor and every motor neuron. So, a sensor on one end of the body can trigger a motor anywhere else on the body. The brain weight matrices are randomly generated.

The method I use to randomly place each new link is described below:
1. A direction is selected, either X, Y, or Z (in the positive or negative). The direction in which the already occupied face points cannot be chosen.
2. Given the current and previous directions of expansion, the relative position of the new joint and link are calculated based on a series of conditional statements. The new joint/link are centered on the chosen face of the previous link.
3. If the current and previous direction are along the same axis, for example both in the x-direction, then the new joint position is expressed as [0, sign_x_direction\*previous_link_size_x_direction, 0]. When the current and previous directions are along different axes, then the new vector has values along those axes with magnitudes of previous_link_size\*0.5. The signs are determinedby the signs of the directions.


*Diagram of overall link addition strategy
![Diagram](https://i.imgur.com/8kSIRv8.jpeg)

# Assignment 6:

Run search.py to recreate results. Creates are created randomly with between 1 and 20 links, with dimensions between 0.2 and 1 (specified in constants.py). If there is no movement, then you happened to generate a snake where none of the sensor links are touching the ground.

# Assignment 5:

The Fitness metric is a weighted sum of two numbers: 1) the greatest number of consecutive time steps that the robot is in the air, and 2) the sum of all time intervals (above some threshold) in which the robot is in the air.

Only maximizing first value evolves robots that do a single very high jump, but they usually fall over afterwards. Adding in the second metric resulted in robots that jumped multiple times.

These values are calculated during the simulation, and most of this logic happens in the Sense() function in robot.py. At the end of the simulation, I calculate the final Fitness by taking a weighted sum of the two metrics specified above.

To achieve my results, I ran batches with population size of 20 and 100 generations. Each batch stored the weights of the single best resulting robot. I ran 20 of these batches, and then used those 20 robots as the starting population for 500 more generations. However, I only did this to test how far these robots could go, and good results can be obtained by just doing 20x100 or 20x500. Run search.py to try it yourself.

# Resources

This project is build on the "LudoBots" evolutionary robotics reddit course, which can be found here: https://www.reddit.com/r/ludobots/
I also use the pyrosim robot simulation library, found here: https://github.com/ccappelle/pyrosim
