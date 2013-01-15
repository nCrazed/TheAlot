from plugins.plugin import PyBotPlugin
import sqlite3

class QuotePlugin(PyBotPlugin):

    def __init__(self):
        self.db = sqlite3.connect('quotes')
        c = self.db.cursor()
        sql = 'CREATE TABLE IF NOT EXISTS quotes (id INTEGER  PRIMARY KEY AUTOINCREMENT, quote STRING)'
        c.execute(sql)
        self.db.commit()
        c.close()

    def parse_user_command(self, bot, command, arguments=None):
        if command == "quoteadd":
            if arguments and self.save_quote(arguments):
                return "Quote saved"
            else:
                return "You suck"
        elif command == "quote":
            if arguments:
                return self.get_quote_with(arguments)
            else:
                return self.get_quote()

        return None

    def get_quote_with(self, search):
        c = self.db.cursor()
        sql = "SELECT quote FROM quotes WHERE quote LIKE ?001 ORDER BY RANDOM() LIMIT 1"
        c.execute(sql, ("%"+search+"%",))
        quote = c.fetchone()
        if quote:
            return quote[0]
        else:
            return "wat is quote"

    def get_quote(self):
        c = self.db.cursor()
        sql = "SELECT quote FROM quotes ORDER BY RANDOM() LIMIT 1"
        c.execute(sql)
        quote = c.fetchone()
        if quote:
            return quote[0]
        else:
            return "wat is quote"

    def save_quote(self, quote):
        c = self.db.cursor()
        sql = "INSERT INTO quotes(quote) VALUES(?)"
        print(quote)
        c.execute(sql, (quote,))
        self.db.commit()
        if c.lastrowid:
            c.close()
            return True
        c.close()

        return False
