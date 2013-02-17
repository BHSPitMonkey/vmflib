#!/usr/bin/python3
"""Example map generator: Outdoor

This script demonstrates vmflib by generating a map with a 2D skybox and
some terrain (a displacement map).

"""
from vmf import *
from vmf.types import Vertex
from vmf.tools import Block

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

# Floor
floor = Block(Vertex(0, 0, -512), (1024, 1024, 64), 'nature/dirtground004')

# Ceiling
ceiling = Block(Vertex(0, 0, 512), (1024, 1024, 64))
ceiling.set_material('tools/toolsskybox2d')

skywalls = []
# Left upper wall
skywalls.append(Block(Vertex(-512, 0, 256), (64, 1024, 512)))
# Right upper wall
skywalls.append(Block(Vertex(512, 0, 256), (64, 1024, 512)))
# Forward upper wall
skywalls.append(Block(Vertex(0, 512, 256), (1024, 64, 512)))
# Rear upper wall
skywalls.append(Block(Vertex(0, -512, 256), (1024, 64, 512)))
for wall in skywalls:
    wall.set_material('tools/toolsskybox2d')

walls = []
# Left wall
walls.append(Block(Vertex(-512, 0, -256), (64, 1024, 512)))
# Right wall
walls.append(Block(Vertex(512, 0, -256), (64, 1024, 512)))
# Forward wall
walls.append(Block(Vertex(0, 512, -256), (1024, 64, 512)))
# Rear wall
walls.append(Block(Vertex(0, -512, -256), (1024, 64, 512)))
# Set each wall's material
for wall in walls:
    wall.set_material('brick/brickwall001')

# Add walls to world geometry
m.world.children.extend(walls)
m.world.children.extend(skywalls)
m.world.children.extend([floor, ceiling])

# TODO: Define a playerspawn entity

# Write the map to a file
m.write_vmf('outdoor.vmf')
