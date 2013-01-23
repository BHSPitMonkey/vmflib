#!/usr/bin/python -i

from vmf import *

m = vmf.ValveMap()

print '\nYou now have a clean ValveMap object to tinker with called "m".'
print 'Try calling m.write_vmf("testmap.vmf") to output it as a VMF file.\n'
print 'Or just type "m" to view the map\'s markup immediately.\n'
print 'CTRL+D to exit.\n'

# Create a new brush
b = brush.Solid()

# Create some sides for the brush and add them to it
s = [brush.Side(), brush.Side(), brush.Side(), brush.Side()]

# TODO: Set up the sides

for side in s:
    b.children.append(side)

# Add brush to map
m.world.children.append(b)
