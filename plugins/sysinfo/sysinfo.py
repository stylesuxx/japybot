import abc, platform
from plugin import Command

class CommandImplementation(Command):
    _name = 'sysinfo'
    _command = 'sys'
    _help = 'Returns information about the system the bot is running on.'
    _description = 'Returns information about the system the bot is running on.'
    _public = False
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
        if isAdmin:
            return platform.platform()