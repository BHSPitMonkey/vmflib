#!/usr/bin/python
"""Example map generator: Outdoor

This script demonstrates vmflib by generating a map with a 2D skybox and
some terrain (a displacement map).

"""
from vmf import *
from vmf.types import Vertex
from vmf.tools import Block

m = vmf.ValveMap()

walls = []

# Floor
floor = Block(Vertex(0, 0, -512), (1024, 1024, 64))

# Ceiling
ceiling = Block(Vertex(0, 0, 512), (1024, 1024, 64))
ceiling.set_material('tools/toolsskybox2d')

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
m.world.children.extend([floor, ceiling])

# TODO: Define a playerspawn entity

# Write the map to a file
m.write_vmf('outdoor.vmf')
