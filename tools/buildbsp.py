#!/usr/bin/python3
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

games = {
    'tf2': {'id': 440},
    'css': {'id': 240},
    'hl2': {'id': 220},
    'hl2mp': {'id': 320},
    'gm': {'id': 4000}
    }
win32 = sys.platform.startswith('win32')
cygwin = sys.platform.startswith('cygwin')
linux = sys.platform.startswith('linux')

def _make_arg_parser():
    parser = argparse.ArgumentParser(description='Build, install, and test a VMF map.')
    parser.add_argument('map')
    parser.add_argument('-g', '--game', default='tf2', choices=games.keys(),
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
    parser.add_argument('--sourcesdk',
        help="location of your sourcesdk folder (for linux/wine)")

    return parser

if __name__ == '__main__':
    parser = _make_arg_parser()
    args = parser.parse_args()
    vmf_file = os.path.abspath(args.map)
    path, filename = os.path.split(vmf_file)
    mapname = filename[:-4]
    mappath = os.path.join(path, mapname)
    bsp_file = os.path.join(path, mapname + ".bsp")
    
    if win32 or cygwin:
        # Define constants
        games['tf2']['gamedir'] = os.path.join("team fortress 2", "tf")
        games['css']['gamedir'] = os.path.join("counter-strike source", "cstrike")
        games['hl2']['gamedir'] = os.path.join("half-life 2", "hl2")
        games['hl2mp']['gamedir'] = os.path.join("half-life 2 deathmatch", "hl2mp")
        games['gm']['gamedir'] = os.path.join("garrysmod", "garrysmod")

        # Environmental scan
        # - Figure out paths we'll need (maybe detect where steam lives?)
        # Best I can figure out for now is accepting a path as an argument
        sourcesdk = os.environ['sourcesdk']
        if cygwin:
            def cygwin2dos(path):
                return subprocess.check_output(["cygpath", '-w', '%s' % path], universal_newlines=True).strip()
            sourcesdk = subprocess.check_output(["cygpath", sourcesdk], universal_newlines=True).strip()
        print(sourcesdk)
        steamapps = os.path.join(sourcesdk, '..')
        sdkbin = os.path.join(sourcesdk, "bin", "orangebox", "bin")
        game = games[args.game]
        gamedir = os.path.join(steamapps, game['gamedir'])
        print(gamedir)
        print(mappath)
        mapsdir = os.path.join(gamedir, "maps")
        if cygwin:
            gamedir = cygwin2dos(gamedir)
            print(gamedir)
            mappath = cygwin2dos(mappath)
            print(mappath)

        # Change working directory first because VBSP is dumb
        os.chdir(os.path.join(sourcesdk, 'bin', 'orangebox'))

        # Run the SDK tools
        vbsp_exe = os.path.join(sdkbin, "vbsp.exe")
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

        vvis_exe = os.path.join(sdkbin, "vvis.exe")
        opts = [vvis_exe]
        if args.fast:
            opts.append('-fast')
        opts.extend(['-game', gamedir, mappath])
        subprocess.call(opts)

        vrad_exe = os.path.join(sdkbin, "vrad.exe")
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
    elif linux:
        # Define constants
        games['tf2']['gamedir'] = os.path.join("Team Fortress 2", "tf")

        # Environmental scan
        sourcesdk = os.path.abspath(args.sourcesdk)
        steamapps = os.path.join(sourcesdk, '..')
        junk, username = os.path.split(os.path.abspath(steamapps))
        sdkbin = os.path.join(sourcesdk, "bin", "orangebox", "bin")
        game = games[args.game]
        gamedir = os.path.join(steamapps, game['gamedir'])

        # Use native maps directory instead of wine's
        mapsdir = os.path.join('~', '.steam', 'steam', 'SteamApps', username, game['gamedir'], "maps")

        # Change working directory first because VBSP is dumb
        os.chdir(os.path.join(sourcesdk, 'bin', 'orangebox'))

        # Environment to use with wine calls
        env = os.environ.copy()
        env['WINEPREFIX'] = "~/.winesteam"

        # Run the SDK tools
        #TODO
        exit(-1)
        
        # Install the map to the game's map directory (unless --no-install)
        if not args.no_install:
            shutil.copy(bsp_file, mapsdir)
        else:
            print("Not installing map")

        # Launch the game (unless --no-run or --no-install)
        if not args.no_run and not args.no_install:
            params = urllib.parse.quote("-dev -console -allowdebug +map %s" % mapname)
            run_url = "steam://run/%d//%s" % (game['id'], params)
            print(run_url)
            webbrowser.open(run_url)
        else:
            print("Not launching game")
    else:
        raise OSError('Your OS is not supported yet!')
