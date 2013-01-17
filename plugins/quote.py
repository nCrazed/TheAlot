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
            if arguments:
                response = self.save_quote(arguments)
                if response:
                    return "Quote saved as {}".format(response)
            return "You suck"

        elif command == "quotedel":
            if arguments and self.delete_quote(arguments):
                return "Quote deleted"
            else:
                return "wat is delete"
        elif command == "quote":
            if arguments:
                return self.get_quote(arguments)
            else:
                return self.get_quote()

        return None

    def delete_quote(self, id):
        c = self.db.cursor()
        sql = "DELETE FROM quotes WHERE id = ?"
        c.execute(sql, (id,))
        if c.rowcount:
            self.db.commit()
            deleted = True
        else:
            deleted = False
            self.db.rollback()
        c.close()
        return deleted

    def get_quote(self, search=""):
        c = self.db.cursor()
        print(search)
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
            return "wat is quote"

    def save_quote(self, quote):
        c = self.db.cursor()
        sql = "INSERT INTO quotes(quote) VALUES(?)"
        c.execute(sql, (quote,))
        self.db.commit()
        if c.lastrowid:
            c.close()
            return c.lastrowid
        c.close()

        return False
