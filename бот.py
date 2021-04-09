import requests
from translate import Translator
from data import *
import discord
from discord.ext import commands

# TOKEN = 'BOT_TOKEN'
# REQUEST = 'URL'


class Find_News:
    def __init__(self):
        self.lang = 'ru'
        self.res = []
        self.reguests = []
        # Team Fortress 2
        # Dota 2
        # Portal 2
        # Counter-Strike: Global Offensive
        self.game_id = {'1': '440',
                        '2': '570',
                        '3': '620',
                        '4': '730'}
        self.game = '2'

    def translate(self, text):
        translator = Translator(to_lang=self.lang)
        return translator.translate(text)

    def make_request(self):
        for i in self.game:
            if i in self.game_id:
                self.reguests.append(REQUEST + f'appid={self.game_id[i]}&count=1&maxlength=300&enddate=33174810590&format=json')

    def set_games(self, new_games):
        del self.reguests[:]
        self.game = new_games
        print(self.game)

    def get_content(self):
        self.make_request()
        del self.res[:]
        for i in self.reguests:
            # Выполняем запрос.
            response = requests.get(i)
            if response:
                # Преобразуем ответ в json-объект
                json_response = response.json()
                toponym = json_response['appnews']['newsitems']
                for i in toponym:
                    self.res.append(i['contents'])
        return self.res

    def get_title_with_url(self):
        self.make_request()
        del self.res[:]
        for i in self.reguests:
            # Выполняем запрос.
            response = requests.get(i)
            if response:
                # Преобразуем ответ в json-объект
                json_response = response.json()
                toponym = json_response['appnews']['newsitems']
                for i in toponym:
                    self.res += [i['title'], i['url']]
        return self.res
            

class Bot_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.find_news = Find_News()

    @commands.command(name='help_bot')
    async def help(self, ctx):
        help_text = '''get_news - выводит новости по желаемой(ым) игре(ам).
set_games <games_id> - устанавливает список желаемых игр,
game_id - id игр, по которм вы хотели бы получать новости
(id вводятся в одну строку БЕЗ каких-либо СИМВОЛОВ РАЗДЕЛЕНИЯ, нпример - "123")
Доступные id игр:
1 - Team Fortress 2
2 - Dota 2
3 - Portal 2
4 - Counter-Strike: Global Offensive'''
        await ctx.send(help_text)

    @commands.command(name='get_news')
    async def get_news(self, ctx):
        await ctx.send('\n'.join(self.find_news.get_title_with_url()))

    @commands.command(name='set_games')
    async def set_games(self, ctx, new_games):
        self.find_news.set_games(str(int(new_games)))
        await ctx.send('Изменения внесены')


bot = commands.Bot(command_prefix='!')
bot.add_cog(Bot_Commands(bot))
bot.run(TOKEN)
