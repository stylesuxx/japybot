import abc
from plugin import Command

class CommandImplementation(Command):
    _name = 'slap'
    _command = 'slap'
    _help = 'Slap somebody with a trout.'
    _description = 'Slap somebody with a trout.'
    _public = True
    _version = "0.1"

    def name(self):
        return self._name

    def version(self):
        return self._version

    def command(self):
        return self._command

    def help(self, isAdmin):
        return self._help

    def description(self):
        return self._description

    def public(self):
        return self._public

    def process(self, args, isAdmin):
        if args != '':
            return '/me slaps ' + args + ' around a bit with a large trout.'
        return ''