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