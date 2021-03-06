japybot
=======

Python Jabber Bot with with easily extensible Plugin System.

# Usage
              python bot.py -h
              usage: bot.py [-h] [-s [SERVER]] [-r [ROOM]] [-n [NICK]] [-p [PASS]] [--reg]
                            JID PASS ADMIN [ADMIN ...]

              Python Jabber Bot.

              positional arguments:
                JID          user@server.de
                PASS         The password
                ADMIN        The bots admins

              optional arguments:
                -h, --help   show this help message and exit
                -s [SERVER]  The conference server
                -r [ROOM]    The room to join
                -n [NICK]    The nick for the room
                -p [PASS]    The password for the room
                --reg        Register Jid if available

# Plugins
There are two types of Plugins:
* Commands: are invoked via a command string and possible parameters
* Parsers: are called for each message

Commands are only invoked if the command string is found on the beginning of the stanza.

Parsers work the same as commands except that every message is passed to them for further procession.

All the Plugins are loaded from the plugin directory when the bot starts up. Until the next reload command the same instance of each plugin is used to process messages and commands.

All zip files in the Plugins directory are extracted and deleted when the plugins are loaded.

This basically means that updating a plugin is as easy as putting the zipped plugin in the plugin folder and then starting or reloading the bot.

Check out the plugins description property if you want to learn more about each plugin. 
