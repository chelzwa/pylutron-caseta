"""LIP protocol layer."""

import asyncio
import json
import logging
import telnetlib

_LOG = logging.getLogger(__name__)


def login(host=None, port=None, username=None, password=None):
    telnet = telnetlib.Telnet(host, port)
    
    """Enter username."""
    telnet.read_until(b'login: ')
    user = username.encode('ascii')
    telnet.write(user + b'\r\n')
    
    """Enter password."""
    telnet.read_until(b'password: ')
    password = password.encode('ascii')
    telnet.write(password + b'\r\n')
    
    telnet.read_until(b'GNET> ')
    
    return LipWriter(telnet)


class LipWriter(object):
    """A wrapper for writing the LIP protocol."""

    def __init__(self, writer):
        """Initialize the writer."""
        self._telnet = writer

    def write(self, cmd):
        """Send a single command."""
        _LOG.debug("Sending: %s" % cmd)

        try:
          self._telnet.write(cmd.encode('ascii') + b'\r\n')
        except BrokenPipeError:
          _LOG.error('BrokenPipeError')
