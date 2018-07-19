#!/usr/bin/env python3
"""A bot to monitor YTS.ag for new movies"""
import sys
import configparser
from tornado.ioloop import IOLoop
from alfred.server import make_app
from alfred.repo import Repository
from alfred.util import logger


def get_config():
    """get app config from config.ini"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    if not config['REPOSITORY']:
        logger.error('Config File Error')
        exit(1)
    return config['REPOSITORY']['URL']

def main():
    """Main command dispatcher."""
    if sys.version_info < (3, 4):
        logger.error('ERROR: Python 3.4+ is required, found Python {}.{}.{}'.format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
        exit(1)

    # repository stuffs
    logger.debug('Initializing Repository')
    repo_url = get_config()
    repo = Repository(repo_url)
    logger.debug(repo.get_url())

    # web server
    logger.debug('Starting web server at port {}'.format(8888))
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()

if __name__ == '__main__':
    main()
