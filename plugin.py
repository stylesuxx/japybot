import abc

class Plugin(object):
    """ This abstact Baseclass has to be implemented by each Plugin. """
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def name(self):
        """ The Plugins name. """
        pass

    @abc.abstractproperty
    def description(self):
        """ The Plugins description. """
        pass

    @abc.abstractproperty
    def version(self):
        """ The Plugins version. """
        pass

class Command(Plugin):
    """ This abstact Baseclass has to be implemented by each Command Plugin. """
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def command(self):
        """ The command string. Alphanumeric, lowercase only. """
        pass

    @abc.abstractproperty
    def help(self):
        """ The Helptext. """
        pass

    @abc.abstractproperty
    def public(self):
        """ Indicates if the reply should be posted to the muc or in private. """
        pass

    @abc.abstractmethod
    def process(self, arguments, isAdmin):
        """ Processes the user input and returns a reply. If the requesting user is an admin, isAdmin is true. """
        return

class Parser(Command):
    """ This abstract Baseclass has to be implemented by each Parser Plugin. """

    @abc.abstractmethod
    def parse(self, message):
        """ Parse the message and do whatever you need to do. """
        return