import abc
from plugin import Parser

class ParserImplementation(Parser):
    _name = 'foo counter'
    _command = 'fc'
    _help = 'Show the foo count.'
    _description = 'Show the foo count'
    _public = True
    _version = "0.1"

    def __init__(self):
        self.count = 0

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
        return 'Foo count: ' + str(self.count)

    def parse(self, msg):
        self.count += msg.count("foo")