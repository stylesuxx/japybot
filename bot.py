import sys, os, thread, xmpp, argparse
from plugin import Plugin, Command, Parser
from pluginLoader import PluginLoader

class Bot:
    def __init__(self, jid, pwd, admins):
        self.jid = xmpp.JID(jid)
        self.user = self.jid.getNode()
        self.domain = self.jid.getDomain()
        self.pwd = pwd
        self.admins = admins
        self.conn = xmpp.Client(self.domain)#, debug=[])
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
        self.conn.RegisterHandler('presence', self.presence)
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

    def join(self, server, channel, nick, pwd):
        """ Join a room on a specific server with a specific nick. """
        room = channel + '@' + server + '/' + nick
        self.ignore.append(channel + '@' + server)

        presence = xmpp.Presence(to=room)
        presence.setTag('x', namespace = xmpp.NS_MUC).setTagData('password', pwd)
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
                    public = self.pluginInstances[cmd].public
                elif cmd == 'help':
                    reply = self.pluginLoader.getHelp(isAdmin)
                elif cmd == 'reload':
                    if isAdmin:
                        self.loadPlugins()
                        reply = 'Reloaded plugins.\nAvailable Plugins: ' + (', ').join(self.pluginInstances.keys())

            # Always post in private when the request was invoked from a chat.
            if msg.getType() == 'chat':
                public = False
            if reply and not public: conn.send(xmpp.Message(msg.getFrom(), reply))
            elif reply and public: conn.send(xmpp.Message(user.getStripped(), reply, typ='groupchat'))

    def presence(self, conn, msg):
        if msg.getType() == 'subscribe':
            jid = msg.getFrom().getStripped()
            self.roster.Authorize(jid)
        if msg.getType() == 'error':
            for admin in self.admins:
                reply = 'Presence Error: ' + msg.getFrom().getStripped() + ' - ' + msg.getError()
                conn.send(xmpp.Message(admin, reply))

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

parser = argparse.ArgumentParser(description='Python Jabber Bot.')
parser.add_argument('user', metavar='JID', type=str, help='user@server.de')
parser.add_argument('pass', metavar='PASS', type=str, help='The password')
parser.add_argument('admins', metavar='ADMIN', type=str, nargs='+', help='The bots admins')
parser.add_argument('-s', dest='server', metavar='SERVER', nargs='?', help='The conference server')
parser.add_argument('-r', dest='room', metavar='ROOM', nargs='?', help='The room to join')
parser.add_argument('-n', dest='nick', metavar='NICK', nargs='?', help='The nick for the room')
parser.add_argument('-p', dest='passRoom', metavar='PASS', nargs='?', help='The password for the room')
#TODO
parser.add_argument('--reg', dest='register', action='store_const', const=True, default=False, help='Register Jid if available')

args = vars(parser.parse_args())
bot = Bot(args['user'], args['pass'], args['admins'])
bot.loadPlugins()
bot.connect()
if args['room'] and args['server'] and args['nick']:
    print 'Joining room'
    bot.join(args['server'], args['room'], args['nick'], args['passRoom'])
bot.loop()