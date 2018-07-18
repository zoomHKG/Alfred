#!/usr/bin/env python3
"""Logger Utility"""

from contextlib import contextmanager
from datetime import datetime
import sys
from traceback import format_exception
import colorama

def color(color_):
    """Utility for ability to disabling colored output."""
    return color_

def warn(title):
    sys.stderr.write(u'{warn}[WARN] {title}{reset}\n'.format(
        warn=color(colorama.Back.RED + colorama.Fore.WHITE
                   + colorama.Style.BRIGHT),
        reset=color(colorama.Style.RESET_ALL),
        title=title))

def exception(title, exc_info):
    sys.stderr.write(
        u'{warn}[WARN] {title}:{reset}\n{trace}'
        u'{warn}----------------------------{reset}\n\n'.format(
            warn=color(colorama.Back.RED + colorama.Fore.WHITE
                       + colorama.Style.BRIGHT),
            reset=color(colorama.Style.RESET_ALL),
            title=title,
            trace=''.join(format_exception(*exc_info))))

def rule_failed(rule, exc_info):
    exception(u'Rule {}'.format(rule.name), exc_info)

def failed(msg):
    sys.stderr.write(u'{red}{msg}{reset}\n'.format(
        msg=msg,
        red=color(colorama.Fore.RED),
        reset=color(colorama.Style.RESET_ALL)))

def debug(msg):
    sys.stderr.write(u'{blue}{bold}[DEBUG]:{reset} {msg}\n'.format(
        msg=msg,
        reset=color(colorama.Style.RESET_ALL),
        blue=color(colorama.Fore.BLUE),
        bold=color(colorama.Style.BRIGHT)))

def error(msg):
    sys.stderr.write(u'{red}{bold}[ERROR]:{reset} {msg}\n'.format(
        msg=msg,
        reset=color(colorama.Style.RESET_ALL),
        red=color(colorama.Fore.RED),
        bold=color(colorama.Style.BRIGHT)))

@contextmanager
def debug_time(msg):
    started = datetime.now()
    try:
        yield
    finally:
        debug(u'{} took: {}'.format(msg, datetime.now() - started))

def version(thefuck_version, python_version):
    sys.stderr.write(
        u'alfred {} using Python {}\n'.format(thefuck_version,
                                              python_version))
