import sys, os, thread, xmpp
from plugin import Plugin, Command, Parser
from pluginLoader import PluginLoader

class Bot:
    def __init__(self, jid, pwd, admins):
        self.jid = xmpp.JID(jid)
        self.user = self.jid.getNode()
        self.domain = self.jid.getDomain()
        self.pwd = pwd
        self.admins = admins.split(',')
        self.conn = xmpp.Client(self.domain, debug=[])
        self.ignore = []
        path = os.getcwd() + '/plugins/'
        self.pluginLoader = PluginLoader(path)
        self.commands = {}
        self.parsers = {}
        self.pluginInstances = {}

    def connect(self):
        """ Connect the bot to the server. """
        conres = self.conn.connect()

        if not conres:
            print "Unable to connect to server %s!" %self.domain
            sys.exit(1)

        if conres<>'tls':
            print "Warning: unable to estabilish secure connection - TLS failed!"

        self.authres = self.conn.auth(self.user, self.pwd, 'pybot')
        if not self.authres:
            print "Unable to authorize on %s - check login/password." %self.domain
            sys.exit(1)
        
        if self.authres<>'sasl':
            print "Warning: unable to perform SASL auth os %s. Old authentication method used!" %self.domain
        
        self.conn.RegisterHandler('message', self.processor)
        #self.conn.RegisterHandler('presence', self.presence)
        self.conn.sendInitPresence()
        self.roster = self.conn.getRoster()

        print "Bot connected to %s" %self.domain

    def loadPlugins(self):
        self.pluginLoader.load()
        self.commands = self.pluginLoader.get(Plugin)
        self.parsers = self.pluginLoader.get(Parser)
        self.pluginInstances = {}
        
        for name in self.commands:
            self.pluginInstances[name] = self.commands[name]()

    def join(self, server, channel, nick):
        """ Join a room on a specific server with a specific nick. """
        room = channel + '@' + server + '/' + nick
        self.ignore.append(channel + '@' + server)

        presence = xmpp.Presence(to=room)
        presence.setTag('x', namespace = xmpp.NS_MUC)#.setTagData('password', '')
        presence.getTag('x').addChild('history',{'maxchars':'0','maxstanzas':'0'})
        self.conn.send(presence)

    def threaded(self, conn, msg):
        """ Process the stanzas. """
        user = msg.getFrom()
        jid = user.getStripped()
        isAdmin = jid in self.admins
        if user not in self.ignore:
            text = msg.getBody()
            reply = ''
            public = False

            if text:
                # Pass message to all parsers
                for name in self.parsers:
                    self.pluginInstances[name].parse(text)

                if text.find(' ') + 1: command, args = text.split(' ', 1)
                else: command, args = text, ''
                
                cmd = command.lower()
                if cmd in self.pluginInstances:
                    reply = self.pluginInstances[cmd].process(args, isAdmin)
                    public = self.pluginInstances[cmd].public()
                elif cmd == 'help':
                    reply = self.pluginLoader.getHelp()
                elif cmd == 'reload':
                    if isAdmin:
                        self.loadPlugins()
                        reply = 'Reloaded plugins.\nAvailable Plugins: ' + (', ').join(self.pluginInstances.keys())

            #self.roster.delItem('stylesuxx@jabber.1337.af/Notebook')
            #self.roster.delItem('stylesuxx@jabber.1337.af')
            
            if user not in self.roster.getItems(): 
                self.roster.Authorize(xmpp.JID(user))
                self.roster.Subscribe(xmpp.JID(user))

            # Always post in private when the request was invoked from a chat.
            if msg.getType() == 'chat':
                public = False

            if reply and not public: conn.send(xmpp.Message(msg.getFrom(),reply))
            elif reply and public: print conn.send(xmpp.Message(user.getStripped(), reply, typ='groupchat'))

    def processor(self, conn, msg):
        """ Handle incomming messages """
        thread.start_new_thread(self.threaded, (conn, msg))

    def loop(self):
        """ Do nothing except handling new xmpp stanzas. """
        try:
            while self.conn.Process(1):
                pass
        except KeyboardInterrupt:
            pass

if len(sys.argv) < 6:
    print "Usage: bot.py username@server.net password nick server channel admin1,admin2,admin3"

else:
    bot = Bot(sys.argv[1], sys.argv[2], sys.argv[6])
    bot.loadPlugins()
    bot.connect()
    bot.join(sys.argv[4], sys.argv[5], sys.argv[3])
    bot.loop()