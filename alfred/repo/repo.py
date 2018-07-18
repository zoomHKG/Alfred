  #!/usr/bin/env python3
"""Alfred Repository Class"""
import logging
from typing import Union, List, Dict

import json

from alfred.exceptions import AlfredError

_LOGGER = logging.getLogger(__name__)


class SerializationError(AlfredError):
    """Error serializing the data to JSON."""


class WriteError(AlfredError):
    """Error writing the data."""

class Repository():
    """ALfred repository"""
    def load_json(self, filename: str, default: Union[List, Dict, None] = None) \
            -> Union[List, Dict]:
        """Load JSON data from a file and return as dict or list.
        Defaults to returning empty dict if file is not found.
        """
        try:
            with open(filename, encoding='utf-8') as fdesc:
                return json.loads(fdesc.read())  # type: ignore
        except FileNotFoundError:
            # This is not a fatal error
            _LOGGER.debug('JSON file not found: %s', filename)
        except ValueError as error:
            _LOGGER.exception('Could not parse JSON content: %s', filename)
            raise AlfredError(error)
        except OSError as error:
            _LOGGER.exception('JSON file reading failed: %s', filename)
            raise AlfredError(error)
        return {} if default is None else default


    def save_json(self, filename: str, data: Union[List, Dict]):
        """Save JSON data to a file.
        Returns True on success.
        """
        try:
            json_data = json.dumps(data, sort_keys=True, indent=4)
            with open(filename, 'w', encoding='utf-8') as fdesc:
                fdesc.write(json_data)
        except TypeError as error:
            _LOGGER.exception('Failed to serialize to JSON: %s',
                              filename)
            raise SerializationError(error)
        except OSError as error:
            _LOGGER.exception('Saving JSON file failed: %s',
                              filename)
            raise WriteError(error)
