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
    def process(self, arguments):
        """ Processes the user input and returns a reply. """
        return