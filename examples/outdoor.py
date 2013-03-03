#!/usr/bin/python3
"""Example map generator: Outdoor

This script demonstrates vmflib by generating a map with a 2D skybox and
some terrain (a displacement map).

"""
from vmf import *
from vmf.types import Vertex
from vmf.tools import Block
from vmf.brush import DispInfo

m = vmf.ValveMap()

# Environment and lighting
m.world.skyname = 'sky_day02_01'
# Sun angle	S Pitch	Brightness		Ambience
# 0 225 0	 -25	 254 242 160 400	172 196 204 80
light = vmf.Entity('light_environment')
light.properties['origin'] = "0 0 0"
light.properties['_ambient'] = "172 196 204 80"
light.properties['_light'] = "254 242 160 400"
light.properties['pitch'] = -25
m.world.children.append(light)

# Displacement map for the floor
# do cool stuff
norms = []
for i in range(17):
    row = []
    for j in range(17):
        row.append(Vertex(0, 0, 1))
    norms.append(row)
dists = []
for i in range(17):
    row = []
    for j in range(17):
        row.append(((i % 2) + ((j+1) % 2)) * 6) # funky pattern
    dists.append(row)
d = DispInfo(4, norms, dists)


# Floor
floor = Block(Vertex(0, 0, -480), (2048, 2048, 64), 'nature/dirtfloor003a')
floor.top().lightmapscale = 32
floor.top().children.append(d)  # Add disp map to the ground

# Ceiling
ceiling = Block(Vertex(0, 0, 512), (2048+128, 2048+128, 64))
ceiling.set_material('tools/toolsskybox2d')

# Prepare some upper walls for the skybox
skywalls = []
# Left upper wall
skywalls.append(Block(Vertex(-1024-64, 0, 128), (64, 2048+128, 768)))
# Right upper wall
skywalls.append(Block(Vertex(1024+64, 0, 128), (64, 2048+128, 768)))
# Forward upper wall
skywalls.append(Block(Vertex(0, 1024+64, 128), (2048+128, 64, 768)))
# Rear upper wall
skywalls.append(Block(Vertex(0, -1024-64, 128), (2048+128, 64, 768)))
for wall in skywalls:
    wall.set_material('tools/toolsskybox2d')

# Prepare some lower walls to be basic walls
walls = []
# Left wall
walls.append(Block(Vertex(-1024, 0, -384), (64, 2048+64, 256)))
# Right wall
walls.append(Block(Vertex(1024, 0, -384), (64, 2048+64, 256)))
# Forward wall
walls.append(Block(Vertex(0, 1024, -384), (2048+64, 64, 256)))
# Rear wall
walls.append(Block(Vertex(0, -1024, -384), (2048+64, 64, 256)))
# Set each wall's material
for wall in walls:
    wall.set_material('brick/brickwall003a')

# Add everything we prepared to the world geometry
m.world.children.extend(walls)
m.world.children.extend(skywalls)
m.world.children.extend([floor, ceiling])

# TODO: Define a playerspawn entity

# Write the map to a file
m.write_vmf('outdoor.vmf')
