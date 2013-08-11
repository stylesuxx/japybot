import abc, time
from plugin import Command

class CommandImplementation(Command):
    _name = 'sleep'
    _command = 'sleep'
    _help = 'Sleep 10 sec.'
    _description = 'Sleep for 10 seconds. This is mostly for testing and debugging purposes.'
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
        time.sleep(10)
        return 'Returning from sleep.'