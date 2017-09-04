#!/usr/bin/env python3

import argparse
import os

from pysteamcli.app_manifest import parse_acf_file


DEFAULT_STEAM_DIR = (
    os.path.join('C:/', 'Program Files (x86)', 'Steam')
    if os.name == 'nt' else
    os.path.join(os.environ['HOME'], '.local', 'share', 'Steam')
)


def get_games(steamapps_dir):

    result = dict()
    for item in os.listdir(steamapps_dir):
        if item.endswith('.acf'):
            manifest = parse_acf_file(os.path.join(steamapps_dir, item))
            result[manifest['AppState']['appid']] = manifest['AppState']['name']
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

    command_group = parser.add_mutually_exclusive_group(required=True)
    command_group.add_argument(
        '-l',
        '--list',
        action='store_true',
        help='List all the games currently installed.'
    )

    namespace = parser.parse_args()
    games = get_games(os.path.join(namespace.steamdir, 'steamapps'))

    if namespace.list:
        for (_, name) in games.items():
            print(name)

if __name__ == "__main__":
    main()
