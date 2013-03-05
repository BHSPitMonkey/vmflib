#!/usr/bin/python3
"""Example map generator: Maze

This script demonstrates vmflib by generating a map that places the player
inside a maze. The maze itself is dynamically generated upon execution of 
this script, and constructed (rather inefficiently) out of cubes. (This could
use some serious optimization, since we end up with many unnecessary faces 
in contact with one another, but for our purposes this is acceptable.)

Note: In Ubuntu, you'll need to apt-get install python3-numpy for this example.

"""
from vmf import *
from vmf.types import Vertex
from vmf.tools import Block
import numpy
from numpy.random import random_integers as rand

# Maze map metrics
maze_block_size = 128 # Hammer units
maze_n = 40 # Maze grid "rows"
maze_m = 40 # Maze grid "columns"
maze_width = maze_block_size * maze_n
maze_height = maze_block_size * maze_m
block_dims = (maze_block_size, maze_block_size, maze_block_size)

# Maze generation, stolen from:
# http://en.wikipedia.org/wiki/Maze_generation_algorithm
def make_maze(width=81, height=51, complexity=.75, density=.75):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density    = int(density * (shape[0] // 2 * shape[1] // 2))
    # Build actual maze
    Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make isles
    for i in range(density):
        x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return Z
maze = make_maze(maze_n, maze_m)

# Floor
floor = Block(Vertex(0, 0, -maze_block_size),
	          (maze_width, maze_height, maze_block_size),
	          'nature/dirtfloor003a')

# Ceiling
ceiling = Block(Vertex(0, 0, maze_block_size),
                (maze_width, maze_height, maze_block_size),
                'tools/toolsskybox2d')

# Maze blocks
blocks = []
for i in range(maze_n):
	for j in range(maze_m):
		if maze[i][j]:
			x = (i * maze_block_size) - (maze_width / 2)
			y = (j * maze_block_size) - (maze_height / 2)
			blocks.append(Block(Vertex(x, y, 0), block_dims))

# Instantiate a new map
m = vmf.ValveMap()

# Add brushes to world geometry
m.world.children.extend(blocks)
m.world.children.append(floor)
m.world.children.append(ceiling)

# TODO: Define team spawn entities at each end of the maze

# Write the map to a file
m.write_vmf('maze.vmf')
