"""

Helper classes specific to creating maps for Team Fortress 2.

"""

from vmf.vmf import Entity, Connections
from vmf.types import Bool, Origin, Output

class GameRules(Entity):
    
    """Sets up game mechanics for TF2.
    
    https://developer.valvesoftware.com/wiki/Tf_gamerules
    
    """
    
    def __init__(self):
        Entity.__init__(self, "tf_gamerules")
        self.origin = "0 0 0"
        self.targetname = "tf_gamerules"
        
        self.hud_type = 0
        self.ctf_overtime = Bool(True)

        self.auto_properties += ['hud_type', 'ctf_overtime']


class LogicKoth(Entity):
    
    """Activates King of the Hill mode.
    
    logic_auto should be the map's source.LogicAuto object
    gamerules should be the map's tf2.GameRules object
    
    https://developer.valvesoftware.com/wiki/Tf_logic_koth
    
    """
    
    def __init__(self, logic_auto, gamerules, respawn_wave_time=6):
        Entity.__init__(self, "tf_logic_koth")
        self.origin = "0 0 0"
        self.targetname = "tf_logic_koth"
        
        self.timer_length = 180  # Seconds needed on team's timer to win
        self.unlock_point = 30   # Seconds after which to enable capping

        self.auto_properties += ['timer_length', 'unlock_point']
        
        # Set up necessary connections
        if logic_auto and gamerules:
            gr = gamerules.targetname
            c = Connections()
            c.children.extend([
                Output("OnMapSpawn", gr, "SetBlueTeamGoalString",
                    "#koth_setup_goal"),
                Output("OnMapSpawn", gr, "SetRedTeamGoalString",
                    "#koth_setup_goal"),
                Output("OnMapSpawn", gr, "SetRedTeamRespawnWaveTime",
                    respawn_wave_time),
                Output("OnMapSpawn", gr, "SetBlueTeamRespawnWaveTime",
                    respawn_wave_time)
            ])
            logic_auto.children.append(c)

class SpawnPoint(Entity):

    """Represents a player spawn point.

    https://developer.valvesoftware.com/wiki/Info_player_teamspawn
    
    """

    def __init__(self, team, origin=(0, 0, 0)):
        Entity.__init__(self, "info_player_teamspawn")

        if team is "red":
            self.properties['TeamNum'] = "2"
        elif team is "blu":
            self.properties['TeamNum'] = "3"

        self.origin = "%d %d %d" % origin
