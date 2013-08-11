import abc
from command import Command

class CommandImplementation(Command):
    _name = 'ping'
    _help = 'Wait for it - pong.'
    _public = True

    def name(self):
        return self._name

    def help(self):
        return self._help

    def public(self):
        return self._public

    def process(self, args):
        return 'pong'