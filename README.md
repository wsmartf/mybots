# mybots
COMP_SCI 396, Artificial Life: Ludobots Tasks  

# Assignment 8:

Run search.py to recreate results. Bodies are randomly generated with 3-7 links. Links are generated one-by-one, and each new link is randomly placed on one of the 5 open faces of the previous one. The shape of each link is determined by assigning random values between 0.2 and 1.5 to each dimension of the rectangle. The joint axes are also randomly assigned, and each joint has 60% freedom of movement, which allows for a wide variety of movement. Theoretically, the body can fill up all of 3D space, as the path of generated links can randomly travel in any direction. 

As the body is constructed, the name of each "sensing" link is stored. To generate the brain, I iterate through these links and make a connection between each sensor and every motor neuron. So, a sensor on one end of the body can trigger a motor anywhere else on the body. The brain weight matrices are randomly generated.

## Link Generation
The method I use to randomly place each new link is described below:
1. A direction is selected, either X, Y, or Z.
2. Given the current and previous directions of expansion, the relative position of the new joint and link are calculated based on a series of conditional statements. The new joint/link are centered on the chosen face of the previous link.
3. If the current and previous direction are along the same axis, for example both in the x-direction, then the new joint position is expressed as [0, previous_link_size_x_direction, 0]. When the current and previous directions are along different axes, then the new vector has values along those axes with magnitudes of previous_link_size\*0.5.

*Diagram of overall link addition strategy for generation*
![Diagram](https://imgur.com/a/wL2Q5ng)

## Robot Evolution
At the start of evolution, 50 random robot morphologies (parents) were generated. Then, 50 generations of mutated robots are generated. During each step, a mutated child is created from the parent. Several features of the robot can mutate: any of the neuron weights, the joint axes (about which axis each joint moves), and the size of the dimensions of each link. Each feature has a specified probability of mutating at any given generation. At each step, the robot in the parent-child pair with the highest fitness "lives on" and is used to produce another child. The fitness is calculated by how much distance the robot moves in the +X direction over the course of the simulation. At the end of the simulation, the parent with the greatest fitness is selected and the GUI simulation is shown.

*Diagram of evolution & mutation*
![Diagram](https://imgur.com/a/bdGzjYq)

*Fitness curves from 5 random simulated evolutions*
![Diagram](https://imgur.com/a/qwWHAkX)

# Resources

This project is build on the "LudoBots" evolutionary robotics reddit course, which can be found here: https://www.reddit.com/r/ludobots/
I also use the pyrosim robot simulation library, found here: https://github.com/ccappelle/pyrosim
