  #!/usr/bin/env python3
"""Alfred Repository Class"""
import logging
import json
import os.path
from typing import Union, List, Dict
from requests import get, exceptions

from alfred.util import logger
from alfred.exceptions import AlfredError

_LOGGER = logging.getLogger(__name__)


class SerializationError(AlfredError):
    """Error serializing the data to JSON."""


class WriteError(AlfredError):
    """Error writing the data."""


class Repository():
    """ALfred repository"""
    notified = []
    def __init__(self, url):
        """Repository Constructor"""
        self.url = url
        self.notified = self.load_notified()


    def load_notified(self):
        """Load already notified movies from file"""
        notified = []
        if os.path.isfile('.notified'):
            with open('.notified', 'r') as file:
                notified = file.read().splitlines()
            logger.debug('.notified loaded.')
            logger.debug(notified)
        else:
            logger.debug('No .notified file found, creating one.')
            open('.notified', 'x')
        return notified


    def save_notified(self, movie):
        """append notified movie to file"""
        with open('.notified', 'a') as file:
            file.write('{}\n'.format(movie))
            file.close()
            self.notified.append(movie)


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


    # def json_to_dict(self, data):
    #     """Convert json to python dictionary"""
    #     try:
    #         return json.loads(data)
    #     except ValueError as error:
    #         logger.exception('Could not parse JSON content: %s', error)
    #         raise AlfredError(error)

    def get_url(self):
        return self.url


    def get_movies(self):
        """Get movies/emails from repo"""
        try:
            res = get(self.url)
            data = res.json()
            filtered_data = dict((k, v) for k, v in data.items() if k not in self.notified)
            return filtered_data
        except ValueError as err:
            logger.error('Could not parse JSON content.')
            raise AlfredError(err)
        except exceptions.ConnectionError as err:
            logger.error('Request Connection Error')
            raise AlfredError(err)
        except Exception as err: # pylint: disable=W0703
            raise AlfredError(err)
