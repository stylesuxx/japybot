import abc
from command import Command

class CommandImplementation(Command):
    _name = 'slap'
    _help = 'Slap somebody with a trout.'
    _public = True

    def name(self):
        return self._name

    def help(self):
        return self._help

    def public(self):
        return self._public

    def process(self, args):
        if args != '':
            return '/me slaps ' + args + ' around a bit with a large trout.'
        return ''