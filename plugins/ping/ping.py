import abc
from plugin import Command

class CommandImplementation(Command):
    _name = 'ping'
    _command = 'ping'
    _help = 'Wait for it - pong.'
    _description = 'Ping - Pong'
    _public = True

    def name(self):
        return self._name

    def command(self):
        return self._command

    def help(self):
        return self._help

    def description(self):
        return self._description

    def public(self):
        return self._public

    def process(self, args):
        return 'pong'