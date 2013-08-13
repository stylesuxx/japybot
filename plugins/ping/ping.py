import abc
from plugin import Command

class CommandImplementation(Command):
    _name = 'ping'
    _command = 'ping'
    _help = 'Wait for it - pong.'
    _description = 'Ping - Pong'
    _public = True
    _version = "0.1"

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def command(self):
        return self._command
    
    @property
    def public(self):
        return self._public

    @property
    def description(self):
        return self._description

    def help(self, isAdmin):
        return self._help

    def process(self, args, isAdmin):
        return 'pong'