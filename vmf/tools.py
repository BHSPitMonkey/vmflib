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

    def __init__(self,
        origin=Vertex(),
        dimensions=(64, 64, 64),
        material='BRICK/BRICKFLOOR001A'):
        """Create a new Block at origin with dimensions and material."""
        self.origin = origin
        self.dimensions = dimensions

        # Create brush
        self.brush = Solid()

        # Create sides
        sides = []
        for i in range(6):
            sides.append(Side(Plane(), material))
        self.brush.children.extend(sides)

        # Compute initial side planes
        self.update_sides()

        # Apply material
        self.set_material(material)

    def update_sides(self):
        """Call this when the origin or dimensions have changed."""
        x = self.origin.x
        y = self.origin.y
        z = self.origin.z
        w, l, h = self.dimensions
        a = w / 2
        b = l / 2
        c = h / 2

        self.brush.children[0].plane = Plane(
            Vertex(x - a, y + b, z + c),
            Vertex(x + a, y + b, z + c),
            Vertex(x + a, y - b, z + c))
        self.brush.children[1].plane = Plane(
            Vertex(x - a, y - b, z - c),
            Vertex(x + a, y - b, z - c),
            Vertex(x + a, y + b, z - c))
        self.brush.children[2].plane = Plane(
            Vertex(x - a, y + b, z + c),
            Vertex(x - a, y - b, z + c),
            Vertex(x - a, y - b, z - c))
        self.brush.children[3].plane = Plane(
            Vertex(x + a, y + b, z - c),
            Vertex(x + a, y - b, z - c),
            Vertex(x + a, y - b, z + c))
        self.brush.children[4].plane = Plane(
            Vertex(x + a, y + b, z + c),
            Vertex(x - a, y + b, z + c),
            Vertex(x - a, y + b, z - c))
        self.brush.children[5].plane = Plane(
            Vertex(x + a, y - b, z - c),
            Vertex(x - a, y - b, z - c),
            Vertex(x - a, y - b, z + c))

    def set_material(self, material):
        for side in self.brush.children:
            side.material = material

    def __repr__(self, tab_level=-1):
        return self.brush.__repr__(tab_level)
