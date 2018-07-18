#!/usr/bin/env python3
"""The exceptions used by alfred."""

class AlfredError(Exception):
    """General Alfred exception occurred."""

    pass


class InvalidEntityFormatError(AlfredError):
    """When an invalid formatted entity is encountered."""

    pass


class NoEntitySpecifiedError(AlfredError):
    """When no entity is specified."""

    pass


class PlatformNotReady(AlfredError):
    """Error to indicate that platform is not ready."""

    pass


class InvalidStateError(AlfredError):
    """When an invalid state is encountered."""

    pass
