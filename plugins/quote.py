from plugins.plugin import Plugin

class QuotePlugin(Plugin):

    help = {
            "quote" : "random quote",
            "quote <text>" : "random quote containing <text>",
            "quote add <text>" : "quote add <text> to quotes",
            "quote delete <number>" : "delete quote with id <number>"
            }

    def hook(self):
        sql = "CREATE TABLE IF NOT EXISTS quotes (id INTEGER PRIMARY KEY AUTOINCREMENT, quote TEXT)"
        c = self.bot.db.cursor()
        c.execute(sql)
        self.bot.db.commit()
        c.close()
        self.bot.commands['quote'] = self.command

    def unhook(self):
        if 'quote' in self.bot.help:
            del self.bot.help['quote']
        if 'quote' in self.bot.commands:
            del self.bot.commands['quote']

    def command(self, source, target, arguments=None):
        if target == self.bot.config['nickname']:
            target = source

        if arguments:
            if arguments[:3] == "add":
                self.notice(source, self.add(arguments[3:]))
            elif arguments[:6] == "delete":
                self.notice(source, self.delete(arguments[6:]))
            else:
                self.message(target, self.quote(arguments))
        else:
            self.message(target, self.quote())

    def add(self, quote):
        if quote:
            c = self.bot.db.cursor()
            sql = "INSERT INTO quotes(quote) VALUES(?)"
            c.execute(sql, (quote,))
            self.bot.db.commit()
            if c.lastrowid:
                id = c.lastrowid
                c.close()
                return "Quote added as {}".format(id)
            else:
                c.close()
                return "Failed to add the quote"
        else:
            return "Nothing to add"

    def delete(self, id):
        if id:
            c = self.bot.db.cursor()
            sql = "DELETE FROM quotes WHERE id = ?"
            c.execute(sql, (id,))
            if c.rowcount:
                self.bot.db.commit()
                c.close()
                return "Quote deleted"
            else:
                self.bot.db.rollback()
                c.close()
                return "Failed to delete"
        else:
            return "Specify quote ID to delete"

    def quote(self, search=""):
        c = self.bot.db.cursor()
        if search:
            sql = "SELECT * FROM quotes WHERE quote LIKE ?001 ORDER BY RANDOM() LIMIT 1"
            c.execute(sql, ("%"+search+"%",))
        else:
            sql = "SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1"
            c.execute(sql)
        quote = c.fetchone()
        if quote:
            return "{}| {}".format(quote[0], quote[1])
        else:
            return "Quote not found"
