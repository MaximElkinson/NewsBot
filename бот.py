import requests
from translate import Translator
from data import *
import discord
from discord.ext import commands
import asyncio


async def loop_func(time_sec, func, *args, **kwargs):
        for _ in range(1000_000_000):
            func(*args, **kwargs)
            await asyncio.sleep(time_sec)
            
# _____ИСКЛЮЧЕНИЯ_____

class NoGame(Exception):
    pass


class NoGameInSpId(NoGame):
    pass


class NoGameInDataBase(NoGame):
    pass

class GameInList(Exception):
    pass


class InputError(Exception):
    pass


class UrlError(Exception):
    pass

# _____КЛАССЫ_____

class Find_News:
    def __init__(self):
        # Язык по умолчанию
        self.lang = 'en'
        # Стек новостей
        self.res = []
        # Стек запросов для получения новостей
        self.reguests = []
        # Словарь игр:
        # 1) Team Fortress 2
        # 2) Dota 2
        # 3) Portal 2
        # 4) Counter-Strike: Global Offensive
        self.game_id = {1: {'index': 440,
                            'name': 'Team Fortress 2',
                            'int_news': 1,
                            'len_content': 300},
                        2: {'index': 570,
                            'name': 'Dota 2',
                            'int_news': 1,
                            'len_content': 300},
                        3: {'index': 620,
                            'name': 'Portal 2',
                            'int_news': 1,
                            'len_content': 300},
                        4: {'index': 730,
                            'name': 'Counter-Strike: Global Offensive',
                            'int_news': 1,
                            'len_content': 300}}
        # Список индексов игр
        self.indexes = [440, 570, 620, 730]
        # Желаемые игры по умолчанию
        self.game = [1]
        # Тип вывода новостей(заголовок и ссылка)
        self.type_with_url = True

    def translate(self, text):
        # функция перевода текста
        # на установленный язык
        if self.lang == 'ru':
            translator = Translator(to_lang='ru')
        return translator.translate(text)

    def set_type_of_return(self):
        # функция смены типа вывода новостей
        if self.type_with_url:
            self.type_with_url = False
        else:
            self.type_with_url = True

    def get_news(self):
        # функция получения новостей
        # Приверка типа вывода новостей
        if self.type_with_url:
            # Получения заголовков и ссылок на новости
            return self.get_title_with_url()
        else:
            # Получение содержания новостей
            return self.get_content()

    def find_new_game(self, new_game):
        # функция поиска новых игр
        # Перевод названия игры в нижни регистр
        name = new_game.lower()
        # Выполнение запроса
        response = requests.get(ALL_GAME)
        # Проверка запроса
        if response:
            # Преобразование ответа в json-объект
            json_response = response.json()
            # Получение словаря с именами и индексами всех игр
            all_games = json_response['applist']['apps']
            for i in all_games:
                # Проверка имени игры
                if i['name'].lower() == name:
                    # Проверка наличия игры в списке игр
                    if i['appid'] not in self.indexes:
                        # Запись игры в список игр
                        self.game_id[len(self.game_id) + 1] = {'index': i['appid'],
                                                                'name': i['name'],
                                                                'int_news': 1,
                                                                'len_content': 300}
                        # Добавление игры в список желаемых игр
                        self.game.append(len(self.game_id))
                        # Возврат "Успех"
                        return True
                    else:
                        # Вызов ошибки
                        raise GameInList()
            # Вызов ошибки
            raise NoGameInDataBase()
        else:
            # Вызов ошибки
            raise UrlError('Ошибка запроса')

    def make_request(self):
        # Функция создания запросов
        for i in self.game:
            if i in self.game_id:
                # Помещение запроса по конкретной игре в стек
                a = self.game_id[i]["index"]
                b = self.game_id[i]["int_news"]
                c = self.game_id[i]["len_content"]
                self.reguests.append(REQUEST + f'appid={a}&count={b}&maxlength={c}&enddate=33174810590&format=json')
            else:
                raise NoGameInSpId('Игра отсутстует в списке игр')

    def set_lang(self):
        # Функция смены языка
        # Проверка действующего языка
        if self.lang == 'en':
            self.lang = 'ru'
        else:
            self.lang = 'en'

    def get_indexes(self):
        # Функция возврата списка индексов игр
        # под которыми они хранятся в программе
        # Создаём пустой список
        sp = []
        for i in self.game_id:
            # Записываем индекс игры в список
            sp.append([self.game_id[i]['name'], i])
        # Возвращаем список
        return sp

    def set_games(self, new_games):
        # Функция изменения желаемых игр
        # Чистим стек и заполням его
        del self.reguests[:]
        self.game = list(map(lambda s: int(s), new_games))

    def set_int_news(self, games, new_int):
        # Функция установки количества новостей
        # по конкретной игре(ам)
        # Проверка на редактирование количества новостей
        # у кождой игры
        if games == 'all':
            # Изменение количества новостей
            # у каждой игры
            for i in self.game_id:
                self.game_id[i]["int_news"] = new_int
        else:
            for i in games:
                # Проверка на наличие иры
                if i in self.game_id:
                    # Изменение количества новостей
                    self.game_id[i]["int_news"] = new_int
                else:
                    # Вызов ошибки
                    raise NoGameInSpId('Игра отсутстует в списке игр')

    def set_len_content(self, games, new_len_content):
        # Функция установки длинны новостей
        # по конкретной игре(ам)
        # Проверка на редактирование длинны новостей
        # у кождой игры
        if games == 'all':
            # Изменение длинны новостей
            # у каждой игры
            for i in self.game_id:
                self.game_id[i]["len_content"] = new_int
        else:
            for i in games:
                # Проверка на наличие иры
                if i in self.game_id:
                    # Изменение длинны новостей
                    self.game_id[i]["len_content"] = new_int
                else:
                    # Вызов ошибки
                    raise NoGameInSpId('Игра отсутстует в списке игр')

    def get_content(self):
        # Функция для получения частей содержаний новостей
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
            else:
                raise UrlError('Ошибка запроса')
        return self.res

    def get_title_with_url(self):
        # Функция для получения заголовков и ссылок на новости
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
            else:
                raise UrlError('Ошибка запроса')
        return self.res

# _____КОМАНДЫ_____

class Bot_Commands(commands.Cog):
    def __init__(self, bot):
        # Наличие автооповещения
        self.timer = False
        # Наличие автоочистки
        self.clean = False
        self.bot = bot
        self.find_news = Find_News()

    @commands.command(name='help_bot')
    async def help(self, ctx):
        if self.clean:
            await ctx.channel.purge(limit=1)
        help_text = '''get_news - выводит новости по желаемой(ым) игре(ам).
set_games <games_id> - устанавливает список желаемых игр,
game_id - id игр, по которм вы хотели бы получать новости
(id вводятся в одну строку БЕЗ каких-либо СИМВОЛОВ РАЗДЕЛЕНИЯ, нпример - "123")'''
        await ctx.send(help_text)

    @commands.command(name='get_indexes')
    async def help(self, ctx):
        if self.clean:
            await ctx.channel.purge(limit=1)
        text = 'Доступные id игр:'
        for i in self.find_news.get_indexes():
            text += f'\n{i[0]} - {i[1]}'
        await ctx.send(text)

    @commands.command(name='get_news')
    async def get_news(self, ctx):
        # Команда для получения новостей
        if self.clean:
            await ctx.channel.purge(limit=1)
        try:
            await ctx.send('\n'.join(self.find_news.get_news()))
        except UrlError:
            await ctx.send('Что-то пошло не так')

    @commands.command(name='set_games')
    async def set_games(self, ctx, *new_games):
        # Команда для установки желаемых игр
        if self.clean:
            await ctx.channel.purge(limit=1)
        # Проверка на провильность ввода
        try:
            self.find_news.set_games(new_games)
        except Exception:
            await ctx.send('Неверный ввод')
        else:
            await ctx.send('Изменения внесены')

    @commands.command(name='set_int_news')
    async def set_int_news(self, ctx, int_news, games='all'):
        # Команда для установки кол-ва новостей
        if self.clean:
            await ctx.channel.purge(limit=1)
        try:
            self.find_news.set_int_news(games, int(int_news))
        except NoGameInSpId:
            await ctx.send('Что-то пошло не так')

    @commands.command(name='set_len_content')
    async def set_len_content(self, ctx, len_content, games='all'):
        # Команда для установки длинны новости(ей)
        if self.clean:
            await ctx.channel.purge(limit=1)
        try:
            self.find_news.set_len_content(games, int(len_content))
        except NoGameInSpId:
            await ctx.send('Что-то пошло не так')

    @commands.command(name='set_type_of_return')
    async def set_type_of_return(self, ctx):
        # Команда для изменения типа вывода новостей
        if self.clean:
            await ctx.channel.purge(limit=1)
        self.find_news.set_type_of_return()


    @commands.command(name='add_game')
    async def add_game(self, ctx, *new_game):
        # Команда для установки желаемых игр
        if self.clean:
            await ctx.channel.purge(limit=1)
        new_game = ' '.join(list(new_game))
        # Проверка на провильность ввода
        try:
            res = self.find_news.find_new_game(new_game)
            if res:
                await ctx.send('Игра добавлена')
            else:
                await ctx.send('Игра не найдена')
        except NoGameInDataBase:
            await ctx.send('Данной игры нет в базе данных')
        except GameInList():
            await ctx.send('Данная ишра уже есть в списке игр')
        except UrlError():
            await ctx.send('Что-то пошло не так')

    @commands.command(name='set_lang')
    async def add_game(self, ctx):
        # Команда для установки желаемых игр
        if self.clean:
            await ctx.channel.purge(limit=1)
        self.find_news.set_lang()
        await ctx.send('Язык изменён')
            

    @commands.command(name='set_timer')
    async def set_timer(self, ctx, time_day):
        if self.clean:
            await ctx.channel.purge(limit=1)
        self.timer = True
        for _ in range(1000_000_000):
            if self.timer:
                try:
                    await ctx.send('\n'.join(self.find_news.get_news()))
                except Exception:
                    await ctx.send('ошибка')
                else:
                    await asyncio.sleep(int(time_day) * 86400)


    @commands.command(name='stop_timer')
    async def stop_timer(self, ctx, time_sec):
        if self.clean:
            await ctx.channel.purge(limit=1)
        if self.timer:
            self.timer = False
            await ctx.send('Автооповещение остановлено')
        else:
            await ctx.send('Автооповещение не установлено')
    

bot = commands.Bot(command_prefix='!')
bot.add_cog(Bot_Commands(bot))
bot.run(TOKEN)
