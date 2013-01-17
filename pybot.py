import importlib
import json
import irc.bot
import irc.strings


COMMAND_PREFIX = "!"

def to_camel_case(s):
    if s.__contains__("_"):
        out = ""
        for part in s.split("_"):
            out += part.title()
        return out
    else:
        return s.title()

class Config:

    def __init__(self, path):
        self.path = path

        print("Reading configuration from %s" % path)
        fh = open(path, 'r')
        self.settings = json.load(fh)
        fh.close()

class PyBot(irc.bot.SingleServerIRCBot):

    def __init__(self):
        self.config = Config("config.json")
        self.plugins = {}

        for name in self.config.settings['plugins']:
            module = __import__("plugins."+name, fromlist=(name))
            print("Loading %sPlugin" % to_camel_case(name))
            self.plugins[name] = getattr(module, to_camel_case(name)+"Plugin")()

        server = self.config.settings['server']
        port = self.config.settings['port']
        nickname = self.config.settings['nickname']
        channel = self.config.settings['channel']
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.connection.buffer_class.errors = 'replace' # Should prevent clients sending messages in latin-1 from craching the client
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        print("Nick in use, appending _")
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        response = self.parse_user_command(e.arguments[0])
        # send response to user

    def on_pubmsg(self, c, e):
        response = self.parse_user_command(e.arguments[0])
        if (response):
            c.privmsg(self.channel, response)

    def parse_user_command(self, msg):
        if msg[0] == COMMAND_PREFIX:
            command = msg[1:].split(" ", 1)
            command[0] = command[0].lower()
            if command[0] == "die":
                self.connection.quit("arggh!")
                exit()
            else:
                for plugin in self.plugins:
                    if len(command) == 1:
                        arguments = None
                    else:
                        arguments = command[1]
                    response = self.plugins[plugin].parse_user_command(self, command[0], arguments)
                    if response:
                        print(response)
                        return response
            return "Invalid command"
        return None



def main():
    # TODO allow passing config path as argument
    bot = PyBot()
    bot.start()

if __name__ == "__main__":
    main()

