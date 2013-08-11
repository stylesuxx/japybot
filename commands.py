import sys, os, inspect, imp
from command import Command

class Commands(object):
    """" Import all available commands from a specific directory. """
    def __init__(self, directory):
        self.commands = {}
        self.directory = directory
        self.name = os.path.basename(os.path.normpath(self.directory))
        self.load()

    def load(self):
        """ This allows to load the plugins from the directory. May also be invoked during runtime. """
        self.commands = {}
        oldcwd = os.getcwd()
        
        for plugin in os.walk(self.directory).next()[1]:
            os.chdir(self.directory + plugin)

            for filename in os.listdir(self.directory + plugin):
                if filename.endswith(".py"):
                    modname = filename[:-3]
                    module = imp.load_source( modname, os.getcwd() + "/" + filename)
                    available = inspect.getmembers(module)
                    
                    for name, obj in available:
                        if inspect.isclass(obj) and issubclass(obj, Command) and not inspect.isabstract(obj):
                            instance = obj()
                            self.commands[instance.command()] = obj

            os.chdir(self.directory)
        os.chdir(oldcwd)

    def getAll(self):
        """ Return a dictionary with all available commands and their classes. """
        return self.commands

    def getHelp(self):
        """ Returns the Helptext for the built in functions and for every installed command. """
        toReturn = "Global Help:\n"
        toReturn += "Built in commands:\n"
        toReturn += 'reload: Reloads the commands directory. Command extensions may be add on runtime.\n'
        toReturn += '--------------\n'
        toReturn += 'Available commands:\n'

        for name in self.commands.keys():
            toReturn += name + ': '
            cmd = self.commands[name]()
            toReturn += cmd.help() + '\n'

        return toReturn

    def reload(self):
        """ Reloads the list of available commands, updates the dictionary and returns all available commands. """
        self.load()
        toReturn = 'Reloaded command list. Available commands:\n'
        toReturn += ', '.join(set(self.commands))

        return toReturn