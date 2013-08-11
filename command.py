import abc

class Command(object):
    """ This abstact Baseclass has to be implemented by each custom Command. """
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def name(self):
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