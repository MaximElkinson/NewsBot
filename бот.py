import requests
import discord
from data import *
from discord.ext import commands

# TOKEN = 'BOT_TOKEN'
# REQUEST = 'URL'

class Find_News:
    def __init__(self):
        pass

    def find(self):
        request = REQUEST
        # Выполняем запрос.
        response = requests.get(request)
        res = []
        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()
            toponym = json_response['appnews']['newsitems']
            for i in toponym:
                res.append(i['contents'])
            return res

class RandomThings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help_bot')
    async def help(self, ctx):
        help_text = ''
        await ctx.send(help_text)

    @commands.command(name='get_news')
    async def translate(self, ctx):
        await ctx.send('\n'.join(Find_News().find()))

bot = commands.Bot(command_prefix='!')
bot.add_cog(RandomThings(bot))
bot.run(TOKEN)