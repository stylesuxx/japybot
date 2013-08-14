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
        """ The Plugins version String. """
        pass

    @abc.abstractmethod
    def help(self, isAdmin):
        """
        Return the Helptext.
        
        :param isAdmin: Indicates if the requesting user is an admin
        """
        pass

class Command(Plugin):
    """ This abstact Baseclass has to be implemented by each Command Plugin. """
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def command(self):
        """ The command string. Alphanumeric, lowercase only. """
        pass

    @abc.abstractproperty
    def public(self):
        """ Indicates if the reply should be posted to the muc or in private. """
        pass

    @abc.abstractmethod
    def process(self, arguments, isAdmin):
        """
        Processes the user input and returns a reply.

        :param arguments: Arguments from the request. This is the remaining string after the command
        :param isAdmin: True if requesting user is an admin
        """
        return

class Parser(Command):
    """ This abstract Baseclass has to be implemented by each Parser Plugin. """

    @abc.abstractmethod
    def parse(self, message):
        """
        Parse the message and do whatever you need to do.

        :param message: The message to parse
        """
        return