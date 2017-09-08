#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

from pysteamcli.app_manifest import parse_acf_file


DEFAULT_STEAM_DIR = (
    os.path.join('C:/', 'Program Files (x86)', 'Steam')
    if os.name == 'nt' else
    os.path.join(os.environ['HOME'], '.local', 'share', 'Steam')
)

DEFAULT_STEAM_EXE = (
    os.path.join(DEFAULT_STEAM_DIR, 'steam.exe')
    if os.name == 'nt' else
    'steam'
)



def get_games(steamapps_dir):

    result = dict()
    for item in os.listdir(steamapps_dir):
        if item.endswith('.acf'):
            manifest = parse_acf_file(os.path.join(steamapps_dir, item))
            result[manifest['AppState']['name']] = manifest['AppState']['appid']
    return result


def main():
    parser = argparse.ArgumentParser(
        prog='pysteamcli',
        description="Use Steam from the comfort of your terminal."
    )

    parser.add_argument(
        '--steamdir',
        type=str,
        help='The installation directory of Steam.',
        default=DEFAULT_STEAM_DIR
    )
    parser.add_argument(
        '--steamexe',
        type=str,
        help='',
        default=DEFAULT_STEAM_EXE
    )

    command_group = parser.add_mutually_exclusive_group(required=True)
    command_group.add_argument(
        '-l',
        '--list',
        action='store_true',
        help='List all the games currently installed.'
    )
    command_group.add_argument(
        '-r',
        '--run',
        type=str,
        help='Game to run.'
    )

    namespace = parser.parse_args()
    games = get_games(os.path.join(namespace.steamdir, 'steamapps'))

    if namespace.list:
        for (name, _) in games.items():
            print(name)

    if namespace.run:
        try:
            rungame = 'steam://rungameid/{appid}'.format(
                appid=games[namespace.run]
            )
        except KeyError:
            print('Error: {} not found!'.format(namespace.run), file=sys.stderr)
            return 1

        return subprocess.call((namespace.steamexe, rungame))

    return 0

if __name__ == "__main__":
    sys.exit(main())
