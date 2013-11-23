"""

Helper classes specific to creating maps for Team Fortress 2.

"""

from vmflib.vmf import Entity, Connections
from vmflib.types import Bool, Origin, Output

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


class MasterControlPoint(Entity):

    def __init__(self):
        Entity.__init__(self, "team_control_point_master")
        self.origin = Origin()
        self.targetname = "master_control_point"

        self.cpm_restrict_team_cap_win = 0
        self.partial_cap_points_rate = 0
        self.play_all_rounds = 0
        self.score_style = 0
        self.switch_teams = 0
        self.team_base_icon_2 = "sprites/obj_icons/icon_base_red"
        self.team_base_icon_3 = "sprites/obj_icons/icon_base_blu"

        self.auto_properties += ["cpm_restrict_team_cap_win",
            "partial_cap_points_rate", "play_all_rounds", "score_style",
            "switch_teams", "team_base_icon_2", "team_base_icon_3"]


class ControlPoint(Entity):

    def __init__(self):
        Entity.__init__(self, "team_control_point")
        self.origin = Origin()

        self.point_default_owner = 0
        self.point_group = 0
        self.point_index = 0
        self.point_printname = "Capture Point"
        self.point_start_locked = 0
        self.point_warn_on_cap = 0
        self.point_warn_sound = "ControlPoint.CaptureWarn"
        self.random_owner_on_restart = 0
        self.team_bodygroup_0 = 3
        self.team_bodygroup_2 = 1
        self.team_bodygroup_3 = 1
        self.team_icon_0 = "sprites/obj_icons/icon_obj_neutral"
        self.team_icon_2 = "sprites/obj_icons/icon_obj_red"
        self.team_icon_3 = "sprites/obj_icons/icon_obj_blu"
        self.team_model_0 = "models/effects/cappoint_hologram.mdl"
        self.team_model_2 = "models/effects/cappoint_hologram.mdl"
        self.team_model_3 = "models/effects/cappoint_hologram.mdl"
        self.team_timedpoints_2 = 0
        self.team_timedpoints_3 = 0 

        self.auto_properties += ["point_default_owner", "point_group",
            "point_index", "point_printname", "point_start_locked",
            "point_warn_on_cap", "point_warn_sound", "random_owner_on_restart",
            "team_bodygroup_0", "team_bodygroup_2", "team_bodygroup_3",
            "team_icon_0", "team_icon_2", "team_icon_3", "team_model_0",
            "team_model_2", "team_model_3", "team_timedpoints_2",
            "team_timedpoints_3"]


class CaptureArea(Entity):

    def __init__(self, capture_point):
        Entity.__init__(self, "trigger_capture_area")

        self.area_cap_point = capture_point.targetname
        self.area_time_to_cap = 10
        self.StartDisabled = 0
        self.team_cancap_2 = 1
        self.team_cancap_3 = 1
        self.team_numcap_2 = 1
        self.team_numcap_3 = 1
        self.team_spawn_2 = 0
        self.team_spawn_3 = 0
        self.team_startcap_2 = 1
        self.team_startcap_3 = 1

        self.auto_properties += ["area_cap_point", "area_time_to_cap",
            "StartDisabled", "team_cancap_2", "team_cancap_3", "team_numcap_2",
            "team_numcap_3", "team_spawn_2", "team_spawn_3", "team_startcap_2",
            "team_startcap_3"]


class HealthKit(Entity):

    def __init__(self, size="medium", origin=(0, 0, 0)):
        if size not in ("small", "medium", "full"):
            raise Exception("Invalid HealthKit size!")
        Entity.__init__(self, "item_healthkit_%s" % size)
        self.origin = Origin(origin)

        self.TeamNum = 0  # 2 for red, 3 for blu

        self.auto_properties += ["TeamNum"]


class AmmoPack(Entity):

    def __init__(self, size="medium", origin=(0, 0, 0)):
        if size not in ("small", "medium", "full"):
            raise Exception("Invalid AmmoPack size!")
        Entity.__init__(self, "item_ammopack_%s" % size)
        self.origin = Origin(origin)

        self.TeamNum = 0  # 2 for red, 3 for blu

        self.auto_properties += ["TeamNum"]

'''
class CaptureArea(Entity):
    
    """Represents a capture zone, as a brush entity."""
    
    def __init__(self):
        Entity.__init__(self, "trigger_capture_area")
'''
