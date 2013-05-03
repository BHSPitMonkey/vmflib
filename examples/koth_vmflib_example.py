#!/usr/bin/python3
"""Example map generator: King of the Hill Example

This script demonstrates vmflib by generating a basic "king of the hill" style
map.  "King of the hill" is a game mode in Team Fortress 2 where each team
tries to maintain control of a central "control point" for some total defined
amount of time (before the other team does).

After this script executes, the map will be written to: koth_vmflib_example.vmf

This example highlights the use of TF2 game mechanics (in this case the use of
a control point and a goal timer). A simple implementation of team
spawn/resupply areas is also included.

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
tf2.LogicKoth(la, gr)

# Environment and lighting (these values come from Sky List on Valve dev wiki)
# Sun angle  S Pitch  Brightness         Ambience
# 0 300 0    -20      238 218 181 250    224 188 122 250
m.world.skyname = 'sky_harvest_01'
light = source.LightEnvironment()
light.set_all("0 300 0", -20, "238 218 181 250", "224 188 122 250")

# Ground
ground = Block(Vertex(0, 0, -32), (2048, 2048, 64), 'nature/dirtground004')
m.world.children.append(ground)

# Skybox
skybox = [
    Block(Vertex(0, 0, 2048), (2048, 2048, 64)),     # Ceiling
    Block(Vertex(-1024, 0, 1024), (64, 2048, 2048)),    # Left wall
    Block(Vertex(1024, 0, 1024), (64, 2048, 2048)),     # Right wall
    Block(Vertex(0, 1024, 1024), (2048, 64, 2048)),     # Forward wall
    Block(Vertex(0, -1024, 1024), (2048, 64, 2048))     # Rear wall
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
    Output("OnCapTeam1", gr.targetname, "SetRedKothClockActive"),  # KOTH-only
    Output("OnCapTeam2", gr.targetname, "SetBlueKothClockActive")  # KOTH-only
])
cp_area.children.append(c)

# Player spawn areas

# Define RED spawn
spawn_red = tf2.SpawnPoint('red', (900, 900, 5))
spawn_red.properties['angles'] = "0 -135 0"

health_red = tf2.HealthKit("full", (950, 910, 0))
health_red.TeamNum = 2

ammo_red = tf2.AmmoPack("full", (910, 950, 0))
ammo_red.TeamNum = 2

# Define BLU spawn
spawn_blu = tf2.SpawnPoint('blu', (-900, -900, 5))
spawn_blu.properties['angles'] = "0 45 0"

health_blu = tf2.HealthKit("full", (-950, -910, 0))
health_blu.TeamNum = 3

ammo_blu = tf2.AmmoPack("full", (-910, -950, 0))
ammo_blu.TeamNum = 3

# Write the map to a file
m.write_vmf('koth_vmflib_example.vmf')
