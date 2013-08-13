import abc, time
from plugin import Command

class CommandImplementation(Command):
    _name = 'sleep'
    _command = 'sleep'
    _help = 'Sleep 10 sec.'
    _description = 'Sleep for 10 seconds. This is mostly for testing and debugging purposes.'
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
    def description(self):
        return self._description

    @property
    def public(self):
        return self._public

    def help(self, isAdmin):
        return self._help

    def process(self, args, isAdmin):
        time.sleep(10)
        return 'Returning from sleep.'