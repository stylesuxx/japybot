import abc, urllib2, re
from plugin import Command

class CommandImplementation(Command):
    _name = 'get'
    _command = 'get'
    _help = 'Get one or more plugins from a remote destination. [get URL1 URL2]'
    _description = 'Enables the admin users to download one or more plugins from a remote destination.'
    _public = False
    _version = "0.1"

    def name(self):
        return self._name

    def version(self):
        return self._version

    def command(self):
        return self._command

    def help(self, isAdmin):
        return self._help

    def description(self):
        return self._description

    def public(self):
        return self._public

    def process(self, args, isAdmin):
        if isAdmin:
            toReturn = "Downloads:\n"
            urls = args.split(' ')
            for url in urls:
                if re.match("^http.*\.zip$", url):
                    try:
                        f = urllib2.urlopen(url)
                        with open("plugins/" + url.split('/')[-1], "wb") as code:
                            code.write(f.read())    
                        toReturn += url + " - OK\n"
                    except urllib2.HTTPError, e:
                        toReturn += url + " - Failed (" + str(e.code) + ")\n"
        return toReturn