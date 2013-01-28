"""

Classes that offer abstractions for brushes, etc. that aren't modeled
in the VMF format itself.

"""

from types import *
from brush import *

class Block():

    """A class representing a 3D block in terms of world geometry.

    This class allows for the simple creation and manipulation of 3D
    blocks (six-sided rectangular prisms) without having to manage
    the underlying brush (Solid) and its faces (Sides) manually.
    You can think of this as the programatic analog to the Block Tool
    in the Valve Hammer Editor.

    """

    def __init__(self, origin=Vertex(), dimensions=(64, 64, 64)):
        self.origin = origin
        self.dims = dimensions

        self.brush = Solid()

        # TODO
