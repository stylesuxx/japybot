import sys, os, inspect

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
        modules = {}
        oldcwd = os.getcwd()
        os.chdir(self.directory)
        for filename in os.listdir(self.directory):
            if filename.endswith(".py"):
                modname = filename[:-3]
                modules[self.directory + '.' + modname] = getattr(__import__(self.name + '.' + modname), modname)
                available = inspect.getmembers(modules[self.directory + '.' + modname])
                for name, obj in available:
                    if name == "CommandImplementation":
                        # TODO: Check if subclass of Command
                        if inspect.isclass(obj):
                            instance = obj()
                            self.commands[instance.name()] = obj
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