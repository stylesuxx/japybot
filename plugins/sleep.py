import abc, time
from command import Command

class CommandImplementation(Command):
    _name = 'sleep'
    _help = 'Sleep 10 sec.'
    _public = True

    def name(self):
        return self._name

    def help(self):
        return self._help

    def public(self):
        return self._public

    def process(self, args):
        time.sleep(10)
        return 'Returning from sleep.'