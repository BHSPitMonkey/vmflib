"""

Helper classes for creating maps in any Source Engine game.

"""

from vmf.vmf import Entity
from vmf.types import Origin

class LogicAuto(Entity):

    """Sets up certain game logic. Fires some useful map events.
    
    https://developer.valvesoftware.com/wiki/Logic_auto
    
    """

    def __init__(self):
        Entity.__init__(self, "logic_auto")
        self.origin = Origin()
        self.spawnflags = 1
