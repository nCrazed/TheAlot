class Plugin:

    def __init__(self, bot):
        self.bot = bot
        self.hook()

    def __del__(self):
        self.unhook()

    def print(self, target, message):
        self.bot.connection.privmsg(target, message)
