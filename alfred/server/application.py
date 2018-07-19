#!/usr/bin/env python3
"""Tornado Application"""
from tornado.web import Application
from .routes import MainHandler

def make_app():
    return Application([
        (r'/', MainHandler)
    ])
