"""

Helper classes specific to creating maps for Team Fortress 2.

"""

from vmf.vmf import Entity


class SpawnPoint(Entity):

    """Represents a player spawn point.

    https://developer.valvesoftware.com/wiki/Info_player_teamspawn
    """

    def __init__(self, team, origin=(0, 0, 0)):
        Entity.__init__(self, 'info_player_teamspawn')

        if team is "red":
            self.properties['TeamNum'] = "2"
        elif team is "blu":
            self.properties['TeamNum'] = "3"

        self.origin = "%d %d %d" % origin
