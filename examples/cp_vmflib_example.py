#!/usr/bin/python3
"""Example map generator: Control Points

This script demonstrates vmflib by generating a basic "control points" style
map.  "Control points" is a game mode in Team Fortress 2 where each team
tries to gain control over all of the control points in a typically symmetrical
environment.  The first team to do this wins.

After this script executes, the map will be written to: cp_vmflib_example.vmf

This example highlights the use of TF2 game mechanics (in this case the use of
multiple control point). A simple implementation of team spawn/resupply areas 
is also included.

https://developer.valvesoftware.com/wiki/Creating_a_Capture_Point
https://developer.valvesoftware.com/wiki/TF2/King_of_the_Hill
"""

from vmf import *
from vmf.types import Vertex, Output, Origin
from vmf.tools import Block
import vmf.games.source as source
import vmf.games.tf2 as tf2

m = vmf.ValveMap()
la = source.LogicAuto()
gr = tf2.GameRules()
#tf2.LogicKoth(la, gr)

# Environment and lighting (these values come from Sky List on Valve dev wiki)
# Sun angle  S Pitch  Brightness         Ambience
# 0 300 0    -20      238 218 181 250    224 188 122 250
m.world.skyname = 'sky_harvest_01'
light = source.LightEnvironment()
light.set_all("0 300 0", -20, "238 218 181 250", "224 188 122 250")

# Ground
ground = Block(Vertex(0, 0, -32), (4096, 4096, 64), 'nature/dirtground004')
m.world.children.append(ground)

# Skybox
skybox = [
    Block(Vertex(0, 0, 4096), (4096, 4096, 64)),     # Ceiling
    Block(Vertex(-2048, 0, 2048), (64, 4096, 4096)),    # Left wall
    Block(Vertex(2048, 0, 2048), (64, 4096, 4096)),     # Right wall
    Block(Vertex(0, 2048, 2048), (4096, 64, 4096)),     # Forward wall
    Block(Vertex(0, -2048, 2048), (4096, 64, 4096))     # Rear wall
]
for wall in skybox:
    wall.set_material('tools/toolsskybox2d')
m.world.children.extend(skybox)

# Control point master entity
cp_master = tf2.MasterControlPoint()

# Control point entity
cp = tf2.ControlPoint()
cp.targetname = "control_point_1"

# Control point prop
cp_prop = vmf.Entity('prop_dynamic')
cp_prop.targetname = "prop_cap_1"
cp_prop.origin = Origin()
cp_prop.properties['model'] = "models/props_gameplay/cap_point_base.mdl"

# Capture area
cp_area = tf2.CaptureArea(cp)
cp_area.children.append(Block(Vertex(0, 0, 128), (256, 256, 256), 
    "TOOLS/TOOLSTRIGGER"))
c = vmf.Connections()
c.children.extend([
    Output("OnCapTeam1", cp_prop.targetname, "Skin", 1),  # Not KOTH-specific
    Output("OnCapTeam2", cp_prop.targetname, "Skin", 2),  # Not KOTH-specific
 #   Output("OnCapTeam1", gr.targetname, "SetRedKothClockActive"),  # KOTH-only
 #   Output("OnCapTeam2", gr.targetname, "SetBlueKothClockActive")  # KOTH-only
])
cp_area.children.append(c)

# Player spawn areas

# Define RED spawn
spawn_red = tf2.SpawnPoint('red', (1900, 1900, 10))
spawn_red.properties['angles'] = "0 -135 0"

# Define BLU spawn
spawn_blu = tf2.SpawnPoint('blu', (-1900, -1900, 10))
spawn_blu.properties['angles'] = "0 45 0"

# Write the map to a file
m.write_vmf('cp_vmflib_example.vmf')
