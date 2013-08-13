japybot
=======

Python Jabber Bot with with easily extensible Plugin System.

# Usage
`python bot.py username@server password nick server channel`

The parameters are quite self explanatory.

# Plugins
There are two types of Plugins:
* Commands: are invoked via a command string and possible parameters
* Parsers: are called for each message

Commands are only invoked if the command string is found on the beginning of the stanza.

Parsers work the same as commands except that every message is passed to them for further procession.

All the Plugins are loaded from the plugin directory when the bot starts up. Until the next reload command the same instance of each plugin is used to process messages and commands.

All zip files in the Plugins directory are extracted and deleted when the plugins are loaded.

# Examples
Check out the plugin interface or take a look in the plugins folder.
