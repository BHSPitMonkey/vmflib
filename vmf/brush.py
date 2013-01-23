"""

Classes for dealing with brushes.

"""

from vmf import Group
from types import *


class Solid(Group):

    """A class representing a single brush in a map.

    You will need to create some Side objects and add them as children
    to your Solid instance. Without Sides (at least four), the brush
    will be invalid.

    """

    classname = 'solid'
    solid_count = 0

    def __init__(self):
        Group.__init__(self)
        self.auto_properties = []

        self.properties['id'] = Solid.solid_count
        Solid.solid_count += 1


class Side(Group):

    """A class representing a single side of a brush."""

    classname = 'side'
    side_count = 0

    def __init__(self):
        Group.__init__(self)
        self.plane = Plane()
        self.material = 'BRICK/BRICKFLOOR001A'
        self.uaxis = '[1 0 0 0] 0.25'
        self.vaxis = '[0 0 -1 0] 0.25'
        self.rotation = 0
        self.lightmapscale = 16
        self.smoothing_groups = 0

        self.auto_properties = ['plane', 'material', 'uaxis', 'vaxis',
            'rotation', 'lightmapscale', 'smoothing_groups']

        p = self.properties
        p['id'] = Solid.solid_count
        Solid.solid_count += 1
