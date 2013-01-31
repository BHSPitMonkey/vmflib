#!/usr/bin/python
"""Example map generator: Woodbox

This script demonstrates vmflib by generating a map (consisting of a large
empty room) and writing it to "woodbox.vmf".  You can open the resulting file
using the Valve Hammer Editor and compile it for use in-game.

This example is a bit convoluted, since we are manually defining every brush
and each of its sides individually. Thankfully, there is now a higher-level
abstraction (tools.Block) which can be used to more easily create 3D block
shapes like the ones shown here. See the example named "woodbox_blocks" for
a demonstration.

"""

from vmf import *

m = vmf.ValveMap()

# Set up brushes for our walls
walls = []
for i in range(6):
    walls.append(brush.Solid())

# Floor
sides = []
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 512, -448),
    types.Vertex(512, 512, -448),
    types.Vertex(512, -512, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, -512, -512),
    types.Vertex(512, -512, -512),
    types.Vertex(512, 512, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 512, -448),
    types.Vertex(-512, -512, -448),
    types.Vertex(-512, -512, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 512, -512),
    types.Vertex(512, -512, -512),
    types.Vertex(512, -512, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 512, -448),
    types.Vertex(-512, 512, -448),
    types.Vertex(-512, 512, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, -512, -512),
    types.Vertex(-512, -512, -512),
    types.Vertex(-512, -512, -448))))
for side in sides:
    side.material = 'PL_BARNBLITZ/WOODWALL_YELLOWWORN002'
walls[0].children.extend(sides)

# Wall 1
sides = []
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, -448, 512),
    types.Vertex(512, -448, 512),
    types.Vertex(512, -512, 512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, -512, -512),
    types.Vertex(512, -512, -512),
    types.Vertex(512, -448, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, -448, 512),
    types.Vertex(-512, -512, 512),
    types.Vertex(-512, -512, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, -448, -512),
    types.Vertex(512, -512, -512),
    types.Vertex(512, -512, 512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, -448, 512),
    types.Vertex(-512, -448, 512),
    types.Vertex(-512, -448, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, -512, -512),
    types.Vertex(-512, -512, -512),
    types.Vertex(-512, -512, 512))))
for side in sides:
    side.material = 'PL_BARNBLITZ/WOODWALL_YELLOWWORN002'
walls[1].children.extend(sides)

# Wall 2
sides = []
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 512, 512),
    types.Vertex(512, 512, 512),
    types.Vertex(512, 448, 512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 448, -512),
    types.Vertex(512, 448, -512),
    types.Vertex(512, 512, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 512, 512),
    types.Vertex(-512, 448, 512),
    types.Vertex(-512, 448, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 512, -512),
    types.Vertex(512, 448, -512),
    types.Vertex(512, 448, 512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 512, 512),
    types.Vertex(-512, 512, 512),
    types.Vertex(-512, 512, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 448, -512),
    types.Vertex(-512, 448, -512),
    types.Vertex(-512, 448, 512))))
for side in sides:
    side.material = 'PL_BARNBLITZ/WOODWALL_YELLOWWORN002'
walls[2].children.extend(sides)

# Wall 3
sides = []
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 448, 448),
    types.Vertex(-448, 448, 448),
    types.Vertex(-448, -448, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, -448, -448),
    types.Vertex(-448, -448, -448),
    types.Vertex(-448, 448, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 448, 448),
    types.Vertex(-512, -448, 448),
    types.Vertex(-512, -448, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-448, 448, -448),
    types.Vertex(-448, -448, -448),
    types.Vertex(-448, -448, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-448, 448, 448),
    types.Vertex(-512, 448, 448),
    types.Vertex(-512, 448, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-448, -448, -448),
    types.Vertex(-512, -448, -448),
    types.Vertex(-512, -448, 448))))
for side in sides:
    side.material = 'PL_BARNBLITZ/WOODWALL_YELLOWWORN002'
walls[3].children.extend(sides)

# Wall 4
sides = []
sides.append(brush.Side(types.Plane(
    types.Vertex(448, 448, 448),
    types.Vertex(512, 448, 448),
    types.Vertex(512, -448, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(448, -448, -448),
    types.Vertex(512, -448, -448),
    types.Vertex(512, 448, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(448, 448, 448),
    types.Vertex(448, -448, 448),
    types.Vertex(448, -448, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 448, -448),
    types.Vertex(512, -448, -448),
    types.Vertex(512, -448, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 448, 448),
    types.Vertex(448, 448, 448),
    types.Vertex(448, 448, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, -448, -448),
    types.Vertex(448, -448, -448),
    types.Vertex(448, -448, 448))))
for side in sides:
    side.material = 'PL_BARNBLITZ/WOODWALL_YELLOWWORN002'
walls[4].children.extend(sides)

# Wall 5
sides = []
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 512, 512),
    types.Vertex(512, 512, 512),
    types.Vertex(512, -512, 512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, -512, 448),
    types.Vertex(512, -512, 448),
    types.Vertex(512, 512, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 512, 512),
    types.Vertex(-512, -512, 512),
    types.Vertex(-512, -512, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 512, 448),
    types.Vertex(512, -512, 448),
    types.Vertex(512, -512, 512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 512, 512),
    types.Vertex(-512, 512, 512),
    types.Vertex(-512, 512, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, -512, 448),
    types.Vertex(-512, -512, 448),
    types.Vertex(-512, -512, 512))))
for side in sides:
    side.material = 'PL_BARNBLITZ/WOODWALL_YELLOWWORN002'
walls[5].children.extend(sides)

# Add walls to world geometry
m.world.children.extend(walls)

# Write the map to a file
m.write_vmf('woodbox.vmf')
