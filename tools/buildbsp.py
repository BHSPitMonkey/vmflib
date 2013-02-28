#!/usr/bin/python3
"""

Utility for building a map using installed Source SDK tools.

Finished use should resemble something like:

  # Creates/installs/runs standard .bsp in same dir
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
    'gm': {'id': 4000}
    }

def _make_arg_parser():
    parser = argparse.ArgumentParser(description='Build a VMF map.')
    parser.add_argument('map')
    parser.add_argument('-g', '--game', default='tf2', choices=games.keys(),
        help="selects which game to use")
    parser.add_argument('--no-run', action="store_true",
        help="don't run the game after building/installing")
    parser.add_argument('--no-install', action="store_true",
        help="don't install (or run) the map after building")
    parser.add_argument('--steamapps',
        help="location of your user's steamapps subfolder")

    return parser

if __name__ == '__main__':
    parser = _make_arg_parser()
    args = parser.parse_args()
    vmf_file = os.path.abspath(args.map)
    path, filename = os.path.split(vmf_file)
    mapname = filename[:-4]
    mappath = os.path.join(path, mapname)
    bsp_file = os.path.join(path, mapname + ".bsp")
    
    if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        # Define constants
        games['tf2']['gamedir'] = os.path.join("team fortress 2", "tf")

        # Environmental scan
        # - Figure out paths we'll need (maybe detect where steam lives?)
        # Best I can figure out for now is accepting a path as an argument
        sourcesdk = os.environ['sourcesdk']
        steamapps = os.path.join(sourcesdk, '..')
        sdkbin = os.path.join(sourcesdk, "bin", "orangebox", "bin")
        game = games[args.game]
        gamedir = os.path.join(steamapps, game['gamedir'])

        # Change working directory first because VBSP is dumb
        os.chdir(os.path.join(sourcesdk, 'bin', 'orangebox'))

        # Run the SDK tools
        # - Use subprocess to call the tools
        vbsp_exe = os.path.join(sdkbin, "vbsp.exe")
        vbsp_cmd = '"%s" -game "%s" "%s"' % (vbsp_exe, gamedir, mappath)
        print(vbsp_cmd)
        subprocess.call(vbsp_cmd)

        # Install the map to the game's map directory (unless --no-install)
        if not args.no_install:
            shutil.copy(bsp_file, os.path.join(gamedir, "maps"))
        else:
            print("Not installing map")

        # Launch the game (unless --no-run or --no-install)
        if not args.no_run and not args.no_install:
            params = urllib.parse.quote("-dev -console -allowdebug +map %s" % "outdoor")
            run_url = "steam://run/%d//%s" % (game['id'], params)
            print(run_url)
            webbrowser.open(run_url)
        else:
            print("Not launching game")

        print("I don't work yet!")        
    else:
        raise OSError('Your OS is not supported yet!')
