from plugins.plugin import Plugin

class LinksPlugin(Plugin):

    help = {
            }

    def hook(self):
        sql = "CREATE TABLE IF NOT EXISTS links (key TEXT PRIMARY KEY, link TEXT)"
        c = self.bot.db.cursor()
        c.execute(sql)
        self.bot.db.commit()
        self.bot.commands['link'] = self.command

    def unhook(self):
        if 'quote' in self.bot.help:
            del self.bot.help['quote']
        if 'quote' in self.bot.commands:
            del self.bot.commands['quote']

    def get_link(self, key):
        c = self.bot.db.cursor()
        sql = "SELECT link FROM links WHERE key LIKE ?"
        c.execute(sql, (key,))
        result = c.fetchone()
        if result:
            return result[0]
        else:
            return "Link not found" #404

    def add(self, key, url):
        c = self.bot.db.cursor()
        sql = "SELECT COUNT(*) FROM links WHERE key LIKE ?"
        c.execute(sql, (key,))
        links = c.fetchone()
        if links[0] == 0:
            sql = "INSERT INTO links(key, link) VALUES(?, ?)"
            c.execute(sql, (key, url))
            if c.lastrowid:
                self.bot.db.commit()
                return "Link added"
        else:
            return "Link already exists"

    def command(self, source, target, arguments=None):
        if target == self.bot.config['nickname']:
            target = source
        message = ""

        if arguments:
            if arguments[:3] == "add":
                try:
                    key, url = arguments[3:].split(maxsplit=1)
                    message = self.add(key, url)
                except ValueError:
                    message = "Expecting two arguments"

            else:
                message = self.get_link(arguments)

        self.message(target, message)
