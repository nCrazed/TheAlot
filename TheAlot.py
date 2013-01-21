import sqlite3
import importlib
import json
import irc.bot
import irc.strings

def to_camel_case(s):
    if s.__contains__("_"):
        out = ""
        for part in s.split("_"):
            out += part.title()
        return out
    else:
        return s.title()

class TheAlot(irc.bot.SingleServerIRCBot):

    def __init__(self, config='config.json'):
        self.configFile = config

        print("Loading configuration from {}".format(config))
        fh = open(config, 'r')
        self.config = json.load(fh)
        fh.close()

        self.db = sqlite3.connect(self.config['database'])

        irc.bot.SingleServerIRCBot.__init__(self, [
            (self.config['server'], self.config['port'])],
            self.config['nickname'],
            self.config['nickname']
        )
        self.connection.buffer_class.errors = 'replace' # Stop clients with latin-1 from craching the bot

        self.initCommands()
        self.plugins = {}
        self.help = {
                "list" : "Display list of commands"
                }

        for plugin in self.config['plugins']:
            module = __import__("plugins."+plugin, fromlist=(plugin))
            name = to_camel_case(plugin) + "Plugin"
            print("Loading {}".format(name))
            self.plugins[plugin] = getattr(module, name)(self)

    def __del__(self):
        try:
            self.db.close()
        except:
            pass

    def initCommands(self):
        self.commands = {
                'help' : self.showHelp,
                'list' : self.listCommands,
                }

    def showHelp(self, source=None, target=None, cmd=None):
        if not cmd:
            self.connection.notice(source, "Usage: help <command>")
        elif cmd in self.help:
            for subcmd in self.help[cmd]:
                self.connection.notice(source, "{:<30} {}".format(subcmd, self.help[cmd][subcmd]))
        else:
            self.connection.notice(source, "No help for that command")

    def listCommands(self, source=None, target=None, args=None):
        for cmd in self.commands:
            self.connection.notice(source, cmd)

    def saveConfig(self, source=None, args=None):
        print(self.config)
        fh = open(self.configFile, "w")
        fh.write(json.dumps(self.config, indent=" "*4))
        fh.close()


    def on_nicknameinuse(self, c, e):
        print("Nick in use, appending _")
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.config['channel'])

    def on_privmsg(self, c, e):
        msg = e.arguments[0]
        if msg[0] != self.config['prefix']:
            msg = self.config['prefix'] + msg
        self.parse_user_command(e.source, e.target, msg)

    def on_pubmsg(self, c, e):
        self.parse_user_command(e.source, e.target, e.arguments[0])

    def parse_user_command(self, source, target, msg):
        if msg[0] == self.config['prefix']:
            command = msg[1:].split(" ", 1)
            command[0] = command[0].lower()
            if command[0] in self.commands:
                if len(command) == 2:
                    self.commands[command[0]](source, target, command[1])
                else:
                    self.commands[command[0]](source, target)
            else:
               self.connection.privmsg(source, "Invalid Command")

def main():
    # TODO allow passing config path as argument
    alot = TheAlot()
    alot.start()

if __name__ == "__main__":
    main()

