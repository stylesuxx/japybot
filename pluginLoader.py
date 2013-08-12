import sys, os, inspect, imp
from plugin import Plugin, Command

class PluginLoader(object):
    """" Import all available Plugins. """
    def __init__(self, directory):
        self.plugins = {}
        self.directory = directory
        self.name = os.path.basename(os.path.normpath(self.directory))

    def get(self, cls):
        """ Get Plugins by class. """
        toReturn = {}
        for name, obj in self.plugins.iteritems():
            if inspect.isclass(obj) and issubclass(obj, cls) and not inspect.isabstract(obj):
                toReturn[name] = obj

        return toReturn                

    def load(self):
        """ Load all the Plugins. """
        self.plugins = {}
        oldcwd = os.getcwd()
        for plugin in os.walk(self.directory).next()[1]:
            os.chdir(self.directory + plugin)
            for filename in os.listdir(self.directory + plugin):
                if filename.endswith(".py"):
                    modname = filename[:-3]
                    module = imp.load_source( modname, os.getcwd() + "/" + filename)
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, Plugin) and not inspect.isabstract(obj):
                            instance = obj()
                            self.plugins[instance.name()] = obj

            os.chdir(self.directory)
        os.chdir(oldcwd)

    def getHelp(self):
        """ Returns the Helptext for the built in functions and for every installed command. """
        toReturn = "Global Help:\n"
        toReturn += "Built in commands:\n"
        toReturn += 'reload: Reloads the commands directory. Command extensions may be add on runtime.\n'
        toReturn += '--------------\n'
        toReturn += 'Available commands:\n'

        for name in self.get(Command):
            toReturn += name + ': '
            cmd = self.plugins[name]()
            toReturn += cmd.help() + '\n'

        return toReturn