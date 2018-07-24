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

def get_credentials():
    """get email credentials from ENV"""
    email = os.environ.get("EMAIL")
    passwd = os.environ.get("PASSWD")
    if not (email and passwd):
        logger.error('EMAIL and PASSWD Environment Variable not set.')
        exit(1)
    return email, passwd


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
def start_scheduler(interval, repo, yts, email):
    """Alfred's life's mission"""
    loop = IOLoop.instance()
    while True:
        logger.debug('Alfred going to bed.')
        yield gen.Task(loop.add_timeout, timedelta(seconds=interval))
        logger.debug('Alfred at work..')
        try:
            wish_list = repo.get_movies()
            available = yts.get_movies()
            # logger.debug(wish_list)
            logger.debug(available)
            for movie in wish_list:
                # logger.debug('{} : {}'.format(movie, movie in available))
                if movie in available:
                    logger.debug('{} Movie available. Sending email.'.format(movie))
                    email.send_mail(wish_list[movie], 'Movie Available',
                                    'The movie {} is now available on YTS.'.format(movie))
                    repo.save_notified(movie)
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
    email, passwd = get_credentials()

    # setup signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # init repository
    repo = Repository(repo_url)
    yts = YTS()

    # init emial
    email = Email(email, passwd)
    email.send_mail(['abhishekmaharjan1993@gmail.com'],
                    'Awake', "I'm awake!! {}".format(repo.notified))

    # scheduler
    start_scheduler(interval, repo, yts, email)

    # web server
    # just a ping endpoint to wake up app from heroku's anesthesia
    start_server()

if __name__ == '__main__':
    main()
