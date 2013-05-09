from plugins.plugin import Plugin

import random

"""
Inspired by http://www.mandatory.com/2013/05/06/the-ultimate-excuse-creator/
"""
class ExcusePlugin(Plugin):

    help = {
            }

    LEADINS = (
            'I\'m sorry but',
            'Please forgive me',
            'Beg you a thousand pardons',
            'I apologize, however',
            'I\'m never usually like this',
            'You\'re never going to believe this',
            'Guess what happened?!?',
            'Holy shit! Get this',
            'Boy o I have a story for you',
            'So I was minding my own business and boom!',
            'The most unbelievable thing just happened',
            'I couldn\'t be more apologetic, but',
            'Sorry I\'m late',
            'I couldn\'t go because',
            'I couldn\'t help it',
            'This is a terrible excuse, but',
            'This is going to sound crazy, but',
            'Holy Moses!',
            'Blimey! Sorry I\'m late guv\'nha',
            'My bad',
            'I swear it wasn\'t my fault',
            'I lost track of time because',
            'I feel terrible, but',
            'Don\'t blame me',
            )
    PERPETRATORS = (
            'your mom',
            'Princess Peach',
            'Godzilla',
            'the offensive line of the \'76 Dallas Cowboys',
            'a handicapped gentleman',
            'a triceratops named Penelope',
            'the inventor of the slanket',
            'the director of 101 Dalmations',
            'the little Asian kid from Indiana Jones',
            'a man with 6 fingers on his right hand',
            'my mom',
            'Raiden from Mortal Kombat',
            'Mayor McCheese',
            'Scrooge McDuck',
            'the ghost of Margaret Thatcher',
            'te ghost of Hitler',
            'Ghost Dad',
            'the entire Roman Empire',
            'Kevin Ware\'s leg bone',
            'a British chap',
            'a Hasidic Jew',
            'Kevin Spacey',
            'Kevin Costner\'s stund double',
            'Kevin McCallister\'s real life fake tarantula',
            'the editors at joinDota',
            'Sun_Tzu',
            )

    FACTORS = (
            'gave me a hickey',
            'tried to kill me',
            'ran me over with a diesel backhoe',
            'died in front of me',
            'ate my homework',
            'tried to seduce me',
            'beat me into submission',
            'hid my Trapper Keeper',
            'stole my bicycle',
            'slep with my uncle',
            'called me "too gay to fly a kite" whatever that means',
            'stole my identity',
            'broke into my house',
            'put me in a Chinese finger trap',
            'came after me',
            'came on me',
            'texted racial slurs from my phone',
            'spin-kicked me in the collar bone',
            'tried to sell me vacuum cleaners',
            'crapepd in my gas tank',
            'made me golf in shoes filled with macaroni and cheese',
            'pulled me over in a stolen cop car and demanded fellatio',
            'made me find Jesus',
            'kept telling me knock knock jokes',
            'fed the enemy carry',
            'killed my courier',
            )

    def hook(self):
        self.bot.commands['excuse'] = self.excuse

    def unhook(self):
        if 'excuse' in self.bot.help:
            del self.bot.help['excuse']
        if 'excuse' in self.bot.commands:
            del self.bot.commands['excuse']

    def excuse(self, source, target, arguments=None):
        if target == self.bot.config['nickname']:
            target = source
        excuse = self.random_element(self.LEADINS) + '... '
        excuse += self.random_element(self.PERPETRATORS) + '... '
        excuse += self.random_element(self.FACTORS) + '.'

        self.message(target, excuse)

    def random_element(self, items):
        return items[random.randrange(len(items))]
