#!/usr/bin/env python3
"""A bot to monitor YTS.ag for new movies"""
import sys
import signal
import configparser
from datetime import timedelta
from tornado import gen
from tornado.ioloop import IOLoop
from alfred.server import make_app
from alfred.repo import Repository
from alfred.util import logger


def get_config():
    """get app config from config.ini"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    if not (config['REPOSITORY'] and config['SCHEDULER']):
        logger.error('Config File Error')
        exit(1)
    return config['REPOSITORY']['URL'], int(config['SCHEDULER']['INTERVAL'])


def signal_handler(signum, frame): # pylint: disable=W0613
    """Signal handler"""
    logger.debug('SIG: {}, Exiting...'.format(signum))
    IOLoop.instance().stop()


def start_server():
    """Start tornado web server"""
    logger.debug('Starting web server at port {}'.format(8888))
    app = make_app()
    app.listen(8888)
    IOLoop.instance().start()

@gen.coroutine
def start_scheduler(interval):
    """Alfred's life's mission"""
    loop = IOLoop.instance()
    while True:
        logger.debug('Alfred going to bed.')
        yield gen.Task(loop.add_timeout, timedelta(seconds=interval))
        logger.debug('Alfred at work..')
        # TODO: fetch movie lists and notify here


def main():
    """Main command dispatcher."""
    if sys.version_info < (3, 4):
        logger.error('ERROR: Python 3.4+ is required, found Python {}.{}.{}'.format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
        exit(1)

    logger.debug('Initializing Repository')
    repo_url, interval = get_config()

    # setup signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # repository stuffs
    repo = Repository(repo_url)
    logger.debug(repo.get_url())

    # scheduler
    start_scheduler(interval)

    # web server
    start_server()

if __name__ == '__main__':
    main()
