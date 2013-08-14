import sys, os, inspect, imp, zipfile
from plugin import Plugin, Command, Parser

class PluginLoader(object):
    """" Import all available Plugins. """
    def __init__(self, directory):
        self.plugins = {}
        self.directory = directory
        self.home = os.getcwd()
        self.name = os.path.basename(os.path.normpath(self.directory))

    def get(self, cls):
        """ Return plugins with the requestet class. """
        return dict((k, v) for k, v in self.plugins.iteritems() if issubclass(v, cls))                

    def load(self):
        """ Load/Reload all the Plugins. """
        os.chdir(self.directory)
        self.plugins = {}

        # Extract present zip archives and remove the archive afterwards.
        for files in [f for f in os.listdir(self.directory) if f.endswith(".zip")]:
            try:
                zipfile.ZipFile(files, "r").extractall()
                os.remove(files)
            except zipfile.BadZipfile:
                pass

        # Build the plugin dictionary
        for plugin in os.walk(self.directory).next()[1]:
            os.chdir(self.directory + plugin)
            for filename in [f for f in os.listdir(self.directory + plugin) if f.endswith(".py")]:
                modname = filename[:-3]
                module = imp.load_source(modname, os.getcwd() + "/" + filename)
                for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, Plugin) and not inspect.isabstract(obj):
                            instance = obj()
                            self.plugins[instance.command] = obj        
        os.chdir(self.home)
    
    def getHelp(self, isAdmin):
        """ Returns the Helptext for the built in functions and for every installed plugin. """
        toReturn = "Global Help:\n"
        toReturn += "Built in commands:\n"
        toReturn += 'reload: Reloads the Plugin directory. Plugins may be add on runtime.\n'
        toReturn += '--------------\n'
        toReturn += 'Available commands:\n'

        for name in self.get(Command):
            toReturn += name + ': ' + self.plugins[name]().help(isAdmin) + '\n'

        return toReturn