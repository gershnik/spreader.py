#!/usr/bin/env python3

import sys
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('type', choices=['release', 'nextpatch', 'nextminor', 'nextmajor'])
parser.add_argument('--dry-run', dest='dryRun', action='store_true')
args = parser.parse_args()


def updateVersion(major, minor, patch, dev):
    if args.type == 'release':
        if not dev:
            patch = int(patch) + 1
        dev = None
    elif args.type == 'nextpatch':
        patch = int(patch) + 1
        dev = 1
    elif args.type == 'nextminor':
        minor = int(minor) + 1
        patch = 0
        dev = 1
    else:
        major = int(major) + 1
        minor = 0
        patch = 0
        dev = 1
    
    return (major, minor, patch, dev)


lines = []
newVersion = None
regex = r'''(?P<prefix>\s*version=["'])(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:\.dev(?P<dev>\d+))?(?P<suffix>["']\s*,?\s*)'''
with open('setup.py', 'r') as setupFile:
    for line in setupFile:
        if newVersion is None:
            m = re.match(regex, line)
            if m:
                groups = m.groupdict()
                major = groups['major']
                minor = groups['minor']
                patch = groups['patch']
                dev = groups.get('dev', None)
                major, minor, patch, dev = updateVersion(major, minor, patch, dev)
                if dev:
                    newVersion = f'{major}.{minor}.{patch}.dev{dev}'
                else:
                    newVersion = f'{major}.{minor}.{patch}'

                line = groups['prefix'] + newVersion + groups['suffix']
                
        lines += line

if newVersion is None:
    print("version line not found", file = sys.stderr)
    sys.exit(1)

if not args.dryRun:
    with open('setup.py', 'w') as setupFile:
        setupFile.writelines(lines)

print(newVersion)

