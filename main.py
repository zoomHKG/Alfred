#!/usr/bin/env python3
"""A bot to monitor YTS.ag for new movies"""
import sys
from alfred import logs


def main():
    """Main command dispatcher."""
    if sys.version_info < (3, 4):
        logs.error('ERROR: Python 3.4+ is required, found Python {}.{}.{}'.format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
    exit(1)

if __name__ == '__main__':
    main()
