import abc
from plugin import Parser

class ParserImplementation(Parser):
    _name = 'foo counter'
    _command = 'fc'
    _help = 'Show the foo count.'
    _description = 'Show the foo count'
    _public = True

    def __init__(self):
        self.count = 0

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

    def process(self, args, isAdmin):
        return 'Foo count: ' + str(self.count)

    def parse(self, msg):
        self.count += msg.count("foo")