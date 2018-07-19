#!/usr/bin/env python3
"""Tornado routes"""
from tornado.web import RequestHandler

class MainHandler(RequestHandler): # pylint: disable=W0223
    """/ hander"""
    def get(self): # pylint: disable=W0221
        """gets app status"""
        self.write('OK')
