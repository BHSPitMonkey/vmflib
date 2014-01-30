#! /usr/bin/env python3
"""

Utility for building a map using installed Source SDK tools.
Call with -h or --help to see usage information.

Examples:

  # Creates/installs/runs .bsp in same dir
  python buildbsp.py --game tf2 mymap.vmf
  
  # Creates/installs .bsp but does not run
  python buildbsp.py --game css --no-run mymap.vmf
  
  # Only create .bsp, and use fast config
  python buildbsp.py --game tf2 --no-run --no-install --fast mymap.vmf

"""
import argparse
import sys
import os
import subprocess
import webbrowser
import urllib.parse
import shutil


class Game:
    def __init__(self, id, dir, common, uses_sdk):
        self.id = id              # Numeric Steam catalog ID number
        self.dir = dir            # Path to inner game directory (containing gameinfo.txt)
        self.common = common      # Game lives under "common" rather than "<username>"
        self.uses_sdk = uses_sdk  # False if game ships with its own map compilers
    def get_game_dir(self, username=False):
        """Returns joined game directory path relative to Steamapps"""
        if not self.common and not username:
            raise RuntimeError("Can't determine this game's directory without username")
        if self.common:
            subdir = "common"
        else:
            subdir = "username"
        subsubdir = self.dir
        if WIN32 or CYGWIN:
            subsubdir = subsubdir.lower()
        return os.path.join(subdir, subsubdir)


WIN32 = sys.platform.startswith('win32')
CYGWIN = sys.platform.startswith('cygwin')
LINUX = sys.platform.startswith('linux')
DARWIN = False  # Not supported yet
GAMES = {
    'tf2': Game(440, os.path.join("Team Fortress 2", "tf"), True, False),
    'css': Game(240, os.path.join("Counter-Strike Source", "cstrike"), False, False),
    'hl2': Game(220, os.path.join("Half-Life 2", "hl2"), False, True),
    'hl2mp': Game(320, os.path.join("Half-Life 2 Deathmatch", "hl2mp"), False, False),
    'gm': Game(4000, os.path.join("GarrysMod", "garrysmod"), False, True),
}

def _make_arg_parser():
    parser = argparse.ArgumentParser(description='Build, install, and test a VMF map.')
    parser.add_argument('map')
    parser.add_argument('-g', '--game', default='tf2', choices=GAMES.keys(),
        help="selects which game to use")
    parser.add_argument('--no-run', action="store_true",
        help="don't run the game after building/installing")
    parser.add_argument('--no-install', action="store_true",
        help="don't install (or run) the map after building")
    parser.add_argument('-f', '--fast', action="store_true",
        help="enable fast compile options")
    parser.add_argument('--hdr', action="store_true",
        help="enable full HDR compile")
    parser.add_argument('--final', action="store_true",
        help="use with --hdr for slow high-quality HDR compile")
    parser.add_argument('--steam-windows-path',
        help="path to your (Windows) Steam folder (for games not dependent on SDK)")
    parser.add_argument('--username',
        help="your Steam username (needed for some games)")

    return parser

def main():
    parser = _make_arg_parser()
    args = parser.parse_args()
    game = GAMES[args.game]
    username = args.username  # May be None
    vmf_file = os.path.abspath(args.map)
    path, filename = os.path.split(vmf_file)
    mapname = filename[:-4]
    mappath = os.path.join(path, mapname)
    bsp_file = os.path.join(path, mapname + ".bsp")
    sourcesdk = None
    winsteam = args.steam_windows_path
    if not winsteam:
        winsteam = os.getenv('winsteam')

    # We need to find out where the SteamApps directory is.
    if winsteam:
        steamapps = os.path.join(winsteam, "Steamapps")
        if not os.path.isdir(steamapps):  # Try lowercase
            steamapps = os.path.join(winsteam, "steamapps")
        if not os.path.isdir(steamapps):
            raise Exception(
                "The provided Steam directory does not contain a Steamapps directory: %s" %
                os.path.abspath(winsteam)
            )
    elif WIN32 or CYGWIN:
        sourcesdk = os.getenv('sourcesdk')
        if CYGWIN:
            def cygwin2dos(path):
                return subprocess.check_output(["cygpath", '-w', '%s' % path], universal_newlines=True).strip()
            sourcesdk = subprocess.check_output(["cygpath", sourcesdk], universal_newlines=True).strip()
        sourcesdk = os.path.abspath(sourcesdk)
        steamapps = os.path.dirname(os.path.dirname(sourcesdk))
        if not os.path.isdir(steamapps):
            raise Exception("Steamapps directory could not be found. Please specify using --steam-windows-path or see --help.")
        if not username:
            username = os.path.basename(os.path.dirname(sourcesdk))
    else:
        raise Exception("Unable to determine where your (Windows) Steam installation is located. See --help.")
    steamapps = os.path.abspath(steamapps)

    # Prepare some useful paths
    gamedir = os.path.join(steamapps, game.get_game_dir(username))
    mapsdir = os.path.join(gamedir, "maps")

    # Get path to correct bin tools directory (game or SDK)
    if game.uses_sdk:
        if not sourcesdk:
            # Try finding SDK within Steamapps
            # TODO
            raise Exception("Sorry, SDK games aren't implemented right now unless you're on Windows.")
        toolsdir = os.path.join(sourcesdk, "bin", "orangebox", "bin")
    else:
        toolsdir = os.path.abspath(os.path.join(gamedir, "..", "bin"))
    
    # Make sure gamedir path seems legit
    if not os.path.isfile(os.path.join(gamedir, "gameinfo.txt")):
        raise Exception("Game directory does not contain a gameinfo.txt: %s" % gamedir)

    if WIN32 or CYGWIN:
        # Convert some paths if using Cygwin
        if CYGWIN:
            gamedir = cygwin2dos(gamedir)
            mappath = cygwin2dos(mappath)

        # Change working directory first because VBSP is dumb
        os.chdir(os.path.join(sourcesdk, 'bin', 'orangebox'))

        # Run the SDK tools
        vbsp_exe = os.path.join(toolsdir, "vbsp.exe")
        code = subprocess.call([vbsp_exe, '-game', gamedir, mappath])
        print("VBSP finished with status %s." % code)

        if code == 1:
            print("Looks like SteamService isn't working. Try reopening Steam.")
            exit(code)
        elif code == -11:
            print("Looks like you might have gotten the 'material not found' " +
                "error messages. Try signing into Steam, or restarting it " +
                "and signing in.")
            exit(code)
        elif code != 0:
            print("Looks like VBSP crashed, but I'm not sure why.")
            exit(code)

        vvis_exe = os.path.join(toolsdir, "vvis.exe")
        opts = [vvis_exe]
        if args.fast:
            opts.append('-fast')
        opts.extend(['-game', gamedir, mappath])
        subprocess.call(opts)

        vrad_exe = os.path.join(toolsdir, "vrad.exe")
        opts = [vrad_exe]
        if args.fast:
            opts.extend(['-bounce', '2', '-noextra'])
        if args.hdr:
            opts.append('-both')
        if args.hdr and args.final:
            opts.append('-final')
        opts.extend(['-game', gamedir, mappath])
        subprocess.call(opts)

        # Install the map to the game's map directory (unless --no-install)
        if not args.no_install:
            print("Copying map %s to %s" % (mapname, mapsdir))
            shutil.copy(bsp_file, mapsdir)
        else:
            print("Not installing map")

        # Launch the game (unless --no-run or --no-install)
        if not args.no_run and not args.no_install:
            params = urllib.parse.quote("-dev -console -allowdebug +map %s" % mapname)
            run_url = "steam://run/%d//%s" % (game['id'], params)
            print(run_url)
            webbrowser.open(run_url)
            if cygwin:
                print("\nYou're running cygwin, so I can't launch the game for you.")
                print("Double-click the URL above, right-click, and click 'Open'.")
                print("Or paste the URL above into the Windows 'Run...' dialog.")
                print("Or, just run 'map %s' in the in-game console." % mapname)
        else:
            print("Not launching game")
    elif LINUX:
        # Environment to use with wine calls
        env = os.environ.copy()
        env['WINEPREFIX'] = os.path.expanduser("~/.winesteam")
        
        # Define path-converting helper function
        def unix2wine(path):
            return subprocess.check_output(["winepath", '-w', '%s' % path], env=env).strip()
        
        # Wine-ify some of our paths
        gamedir = unix2wine(gamedir)
        mappath = unix2wine(mappath)

        # Tell wine to look for DLLs here
        #env['WINEDLLPATH'] = os.path.join(sourcesdk, "bin")
        
        #print("WINEDLLPATH is as follows: ", env['WINEDLLPATH'])

        # Use native maps directory instead of the Wine installation's
        mapsdir = os.path.join('~', '.steam', 'steam', 'SteamApps', game.get_game_dir(username), "maps")
        mapsdir = os.path.expanduser(mapsdir)

        # Change working directory first because VBSP is dumb
        #os.chdir(os.path.join(sourcesdk, 'bin', 'orangebox'))
        
        print("Using -game dir: %s" % gamedir)
        
        # We now need to set the VPROJECT env variable
        env['VPROJECT'] = gamedir

        # Run the SDK tools
        vbsp_exe = os.path.join(toolsdir, "vbsp.exe")
        code = subprocess.call(['wine', vbsp_exe, '-game', gamedir, mappath], env=env)
        print("VBSP finished with status %s." % code)

        # Handle various exit status codes VBPS may have returned
        if code == 1:
            print("\nLooks like VBSP crashed, possibly due to invalid geometry in the map. Check the output above.")
            print("\It could also be related to SteamService isn't working. Try re(launching) wine's Steam:")
            steambin = os.path.join(os.path.dirname(steamapps), 'steam.exe')
            print('\nWINEPREFIX="%s" wine "%s" -no-dwrite' % (env['WINEPREFIX'], steambin))
            exit(code)
        elif code == -11:
            print("\nLooks like you might have gotten the 'material not found' " +
                "error messages. Try signing into Steam, or restarting it " +
                "and signing in.")
            exit(code)
        elif code != 0:
            print("\nLooks like VBSP crashed, but I'm not sure why.")
            exit(code)

        vvis_exe = os.path.join(toolsdir, "vvis.exe")
        opts = ['wine', vvis_exe]
        if args.fast:
            opts.append('-fast')
        opts.extend(['-game', gamedir, mappath])
        code = subprocess.call(opts, env=env)

        if code != 0:
            print("\nLooks like VVIS crashed, but I'm not sure why.")
            exit(code)

        vrad_exe = os.path.join(toolsdir, "vrad.exe")
        opts = ['wine', vrad_exe]
        if args.fast:
            opts.extend(['-bounce', '2', '-noextra'])
        if args.hdr:
            opts.append('-both')
        if args.hdr and args.final:
            opts.append('-final')
        opts.extend(['-game', gamedir, mappath])
        code = subprocess.call(opts, env=env)
        
        if code != 0:
            print("\nLooks like VRAD crashed, but I'm not sure why.")
            exit(code)

        # Install the map to the game's map directory (unless --no-install)
        if not args.no_install:
            shutil.copy(bsp_file, mapsdir)
        else:
            print("Not installing map")

        # Launch the game (unless --no-run or --no-install)
        if not args.no_run and not args.no_install:
            params = urllib.parse.quote("-dev -console -allowdebug +map %s" % mapname)
            run_url = "steam://run/%d//%s" % (game.id, params)
            print(run_url)
            webbrowser.open(run_url)
        else:
            print("Not launching game")
    else:
        raise OSError('Your OS is not supported yet!')

if __name__ == '__main__':
    main()
