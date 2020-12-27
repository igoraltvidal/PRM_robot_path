# PRM - Probabilistic Road Maps

## Introduction

This is a simple example to show the Probabilistic Road Maps, an approach to find a path for a mobile robot.
This repository is part of a project for the Autonomous Robots' signature at the master in Artificial Intelligence/UPM. 
The program looks like a maze solver.

![](https://github.com/igoraltvidal/PRM_robot_path/blob/main/maze3_gif.gif)


## Development

The algorithm solves the problem to find a path using nodes and edges. Nodes are placed randomly at the maze and edges are found
in order to connect two nodes. Then a init and target point are set, the algorithm uses some kind of A* approach to finding a path.
The algorithm follows 4 steps:

### Step 1

Create the nodes, the user set as an argument (argv2) the desired number of nodes. The nodes are placed randomly. The node is
only placed if the space is empty.

```
while numberOfNodes(graph) < desiredNumNodes:
    q = random configuration
    if q is collision free:
    addNode(q,graph)
```

### Step 2

The second step is to find the connections between the nodes (edges). The edges are created only if the line doesn't collide with
any wall of the maze. Some optimization techniques are used to minimize the time to process the nodes. A summary of the 
algorithms used to optimize is listed below:

* The nodes are generated sequentially, the maze is divided into 9 imaginary squares, one square per time will randomly
generate nodes. This approach allows a better organization between the nodes generated. When the nodes are looking for another node
to create an edge, then the node will already know the closest neighbors.
* There are several edges that each node will create, a function optimize these numbers and keep only the edges with the
the smallest distance between nodes.

```
forall q in nodes(graph):
neighborsQ = k closest neighbors to q in graph using some metric
forall r in neighborsQ:
if (q,r) 6∈ edges(graph) and pathExists(q,r):
addEdge(graph,q,r)
```

### Step 3

The program will get the mouse position for the init node and the goal node.

```
neighQStart = k closest neighbors to qstart in graph using some metric
neighQGoal = k closest neighbors to qgoal in graph using some metric
addNode(qstart,graph); addNode(qgoal,graph)
r = closest neighbor to qstart in neighQStart
```

### Step 4

The program will use a modified A* to find the best path. The gray node is never reached, the yellow node was already crossed,
the red node is the actual node performing the calculations, the green node is part of the best path.

```
repeat:
if pathExists(qstart,r):
addEdge(graph,qstart,r)
else:
r = next closest neighbor in neighQStart
until new edge added or no more neighbors in neighQStart
. . . Same with qgoal to connect it into graph . . .
if pathExists(qstart,qgoal,graph):
return path
else:
return fail
```

## Modified A-star

The classic A-star is basically a multiplication between the (distance_to_goal) and (distance_to_next_node), this project includes another heuristic, that is the (times_algorithm_crossed_that_node) * constant. This makes the algorithm try new paths.

## How to use

The program needs two arguments, the first is the maze the user wants, there are five options:

* maze1
* maze2
* maze3
* maze4
* maze5

The second argument is the number of nodes the user wants. Example using maze3 and 500 nodes:

```
python main.py maze3 500
```

## Future jobs

* Improve the nodes optimization
* Improve the A-start with more variables, like the weight for paths with walls



