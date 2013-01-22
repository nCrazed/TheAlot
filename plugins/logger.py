from plugins.plugin import Plugin

class LoggerPlugin(Plugin):

    help = {
            }

    def hook(self):
        sql = "CREATE TABLE IF NOT EXISTS logger (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATETIME, source TEXT, message TEXT)"
        c = self.bot.db.cursor()
        c.execute(sql)
        self.bot.db.commit()
        c.close()
        self.bot.hookEvent("pubmsg", self.on_message)

    def unhook(self):
        self.bot.unhookEvent("pubmsg", self.on_message)

    def on_message(self, source=None, target=None, args=None):
        print("<{}> {}".format(source, args))
        c = self.bot.db.cursor()
        sql = "INSERT INTO logger(date, source, message) VALUES(datetime('now'), ?, ?)"
        c.execute(sql, (source, args))
        self.bot.db.commit()
        c.close()
