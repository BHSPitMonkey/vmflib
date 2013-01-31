#!/usr/bin/python
"""Example map generator: Woodbox (Block)

This script demonstrates vmflib by generating a map (consisting of a large
empty room) and writing it to "woodbox_block.vmf". You can open the resulting
file using the Valve Hammer Editor and compile it for use in-game.

This example shows off the tools.Block class, which allows for the easy
creation of 3D block brushes. It's pretty awesome.

"""
from vmf import *
from vmf.types import Vertex
from vmf.tools import Block

m = vmf.ValveMap()

walls = []

# Floor
walls.append(Block(Vertex(0, 0, -512), (1024, 1024, 64)))

# Ceiling
walls.append(Block(Vertex(0, 0, 512), (1024, 1024, 64)))

# Left wall
walls.append(Block(Vertex(-512, 0, 0), (64, 1024, 1024)))

# Right wall
walls.append(Block(Vertex(512, 0, 0), (64, 1024, 1024)))

# Forward wall
walls.append(Block(Vertex(0, 512, 0), (1024, 64, 1024)))

# Rear wall
walls.append(Block(Vertex(0, -512, 0), (1024, 64, 1024)))

# Set each wall's material
for wall in walls:
    wall.set_material('PL_BARNBLITZ/WOODWALL_YELLOWWORN002')

# Add walls to world geometry
m.world.children.extend(walls)

# TODO: Define a playerspawn entity

# Write the map to a file
m.write_vmf('woodbox_block.vmf')
