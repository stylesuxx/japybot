import abc
from plugin import Command

class CommandImplementation(Command):
    _name = 'slap'
    _command = 'slap'
    _help = 'Slap somebody with a trout.'
    _description = 'Slap somebody with a trout.'
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
        if args != '':
            return '/me slaps ' + args + ' around a bit with a large trout.'
        return ''