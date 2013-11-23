"""

Helper classes for creating maps in any Source Engine game.

"""

from vmflib.vmf import Entity
from vmflib.types import Origin

class LightEnvironment(Entity):
    
    """Casts environmental light from all skybox2d textures in a map.

    https://developer.valvesoftware.com/wiki/Light_environment

    """

    def __init__(self):
        Entity.__init__(self, "light_environment")
        self.origin = Origin()

        self.pitch = 0
        self.angles = Origin()
        self._light = "255 255 255 250"
        self._ambient = "155 155 155 250"
        self._lightHDR = "-1 -1 -1 1"       # Will use same as LDR
        self._lightscaleHDR = "1"
        self._ambientHDR = "-1 -1 -1 1"     # Will use same as LDR
        self._AmbientScaleHDR = "1"

        self.auto_properties += ["pitch", "angles", "_light", "_ambient",
            "_lightscaleHDR", "_lightHDR", "_AmbientScaleHDR", "_ambientHDR"]

    def set_all(self, angles, pitch, brightness, ambience):
        self.angles = angles
        self.pitch = pitch
        self._light = brightness
        self._ambient = ambience

    def set_hdr(self, brightness, brightness_scale, ambience, ambience_scale):
        self._lightHDR = brightness
        self._lightscaleHDR = brightness_scale
        self._ambientHDR = ambience
        self._AmbientScaleHDR = ambience_scale

class LogicAuto(Entity):

    """Sets up certain game logic. Fires some useful map events.

    https://developer.valvesoftware.com/wiki/Logic_auto

    """

    def __init__(self):
        Entity.__init__(self, "logic_auto")
        self.origin = Origin()
        self.spawnflags = 1
