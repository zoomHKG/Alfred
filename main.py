#!/usr/bin/env python3
"""A bot to monitor YTS.ag for new movies"""
import os
import sys
import signal
import configparser
from datetime import timedelta
from tornado import gen
from tornado.ioloop import IOLoop
from alfred.server import make_app
from alfred.repo import Repository
from alfred.util import logger
from alfred.notify import Email
from alfred.sources.yts import YTS

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
    sys.exit(0)


def start_server():
    """Start tornado web server"""
    port = os.environ.get("PORT", 5000)
    logger.debug('Starting web server at port {}'.format(port))
    app = make_app()
    app.listen(port)
    IOLoop.instance().start()

@gen.coroutine
def start_scheduler(interval, repo, yts):
    """Alfred's life's mission"""
    loop = IOLoop.instance()
    while True:
        logger.debug('Alfred going to bed.')
        yield gen.Task(loop.add_timeout, timedelta(seconds=interval))
        logger.debug('Alfred at work..')
        # TODO: fetch movie lists and notify here
        try:
            wish_list = repo.get_movies()
            available = yts.get_movies()
            logger.debug(available)
            for movie in wish_list:
                if movie in available:
                    logger.debug('{} Movie available. Sending email.')
                    # TODO: send email
        except Exception: # pylint: disable=W0703
            logger.error('Failed to fetch movie list from repo')


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

    # init repository
    repo = Repository(repo_url)
    yts = YTS()

    # scheduler
    start_scheduler(interval, repo, yts)

    # web server
    # just a ping endpoint to wake up app from heroku's anesthesia
    start_server()

if __name__ == '__main__':
    main()
