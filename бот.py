import requests
from translate import Translator
from data import *
import discord
from discord.ext import commands
import asyncio


            
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
        self.game_id = [{'index': 440,
                         'name': 'Team Fortress 2',
                         'int_news': 1,
                         'len_content': 300},
                        {'index': 570,
                         'name': 'Dota 2',
                         'int_news': 1,
                         'len_content': 300},
                        {'index': 620,
                         'name': 'Portal 2',
                         'int_news': 1,
                         'len_content': 300},
                        {'index': 730,
                         'name': 'Counter-Strike: Global Offensive',
                         'int_news': 1,
                         'len_content': 300}]
        # Список индексов игр
        self.indexes = [440, 570, 620, 730]
        # Желаемые игры по умолчанию
        self.game = [1]
        # Тип вывода новостей(заголовок и ссылка)
        self.type_with_url = True

    def translate(self, text):
        # функция перевода текста
        # на установленный язык
        # Проверка на установку русского языка
        # (все новости изначально на английском)
        if self.lang == 'ru':
            # Перевод текста
            translator = Translator(to_lang='ru')
            return translator.translate(text)
        else:
            return text

    def set_type_of_return(self):
        # функция смены типа вывода новостей
        if self.type_with_url:
            # Выводить содержание новости
            # в следующих запросах
            self.type_with_url = False
        else:
            # Выводить заголовок и ссылку на новость
            # в следующих запросах
            self.type_with_url = True

    def get_news(self):
        # функция получения новостей
        # Очистка масивов
        del self.res[:]
        del self.reguests[:]
        # Проверка типа вывода новостей
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
                        self.game_id.append({'index': i['appid'],
                                             'name': i['name'],
                                             'int_news': 1,
                                             'len_content': 300})
                        # Добавление игры в список желаемых игр
                        self.game.append(len(self.game_id))
                        self.indexes.append(i['appid'])
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
            if i <= len(self.game_id):
                # Помещение запроса по конкретной игре в стек
                a = self.game_id[i - 1]["index"]
                b = self.game_id[i - 1]["int_news"]
                c = self.game_id[i - 1]["len_content"]
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
        # Функция возврата списка индексов игр,
        # под которыми они хранятся в программе
        # Создаём пустой список
        sp = []
        for i in self.game_id:
            # Записываем индекс игры в список
            sp.append([self.game_id.index(i) + 1, i['name']])
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
        # у каждой игры
        if games == 'all':
            # Изменение количества новостей
            # у каждой игры
            for i in self.game_id:
                i["int_news"] = new_int
        else:
            for i in games:
                # Проверка на наличие игры
                if i <= len(self.game_id):
                    # Изменение количества новостей
                    self.game_id[i - 1]["int_news"] = new_int
                else:
                    # Вызов ошибки
                    raise NoGameInSpId('Игра отсутстует в списке игр')

    def set_len_content(self, games, new_len_content):
        # Функция установки длины новостей
        # по конкретной игре(ам)
        # Проверка на редактирование длины новостей
        # у кождой игры
        if games == 'all':
            # Изменение длины новостей
            # у каждой игры
            for i in self.game_id:
                i["len_content"] = new_len_content
        else:
            for i in games:
                # Проверка на наличие игры
                if i <= len(self.game_id):
                    # Изменение длины новостей
                    self.game_id[i - 1]["len_content"] = new_len_content
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

    def delete_game(self, game):
        del self.game_id[game - 1]
        for i in range(len(self.game)):
            if self.game[i] == game - 1:
                del self.game[i]
            elif self.game[i] > game - 1:
                self.game[i] -= 1

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
        # Команда для вывода инструкции для бота
        if self.clean:
            await ctx.channel.purge(limit=1)
        help_text = '''get_news - выводит новости по желаемой(ым) игре(ам).
set_games <индексы игр> - устанавливает список желаемых игр
(id вводятся через пробел)
get_indexes - выводит индексы поддерживаемых игр
set_int_news <кол-во новостей> <индексы игр> - изменяет кол-во выводимых новостей по некоторым играм
set_content_length <длинна новостей> <индексы игр> - изменяет длинну выводимых новостей по некоторым играм
set_type_of_return - изменяет формат вывода новостей
add_game <название игры> - добавляет новую игру к списку поддерживаемых игр
set_language - изменяет язык заголовков новостей
set_timer <кол-во дней> - устанавливает автооповещение
stop_timer - останавливает автооповещение
toggle_cleaning - устанавливает автоочистку ненужных команд
delete_game <индекс игры> - удаляет игру из списка поддерживаемых игр'''
        await ctx.send(help_text)

    @commands.command(name='get_indexes')
    async def get_indexes(self, ctx):
        # Команда для получения индексов
        # поддерживаемых игр
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
        news = '\n'.join(self.find_news.get_news())
        # ЗАМОРОЖЕНО
        # emb = discord.Embed(title='Новости', color=discord.Color.green())
        # emb.add_field(name=news, value="undefined", inline=False)
        # emb.set_image(url='https://e.sfu-kras.ru/pluginfile.php/1794713/course/overviewfiles/%D0%9B%D0%BE%D0%B3%D0%BE%D1%82%D0%B8%D0%BF.jpg')
        # emb.set_thumbnail(url='https://e.sfu-kras.ru/pluginfile.php/1794713/course/overviewfiles/%D0%9B%D0%BE%D0%B3%D0%BE%D1%82%D0%B8%D0%BF.jpg')
        try:
            # await ctx.send('\n'.join(self.find_news.get_news()))
            await ctx.send(news)
        except UrlError:
            await ctx.send('Что-то пошло не так')

    @commands.command(name='set_games')
    async def set_games(self, ctx, *new_games):
        # Команда для установки желаемых игр
        if self.clean:
            await ctx.channel.purge(limit=1)
        # Проверка на правильность ввода
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

    @commands.command(name='set_content_length')
    # @commands.command(name='scl')
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
    # @commands.command(name='ag')
    async def add(self, ctx, *new_game):
        # Команда для добавления новых игр
        if self.clean:
            await ctx.channel.purge(limit=1)
        new_game = ' '.join(list(new_game))
        # Проверка на правильность ввода
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

    @commands.command(name='set_language')
    # @commands.command(name='sl')
    async def set_lang(self, ctx):
        # Команда для изменения языка
        if self.clean:
            await ctx.channel.purge(limit=1)
        self.find_news.set_lang()
        await ctx.send('Язык изменён')
            

    @commands.command(name='set_timer')
    async def set_timer(self, ctx, time_day):
        # Команда для запуска таймера
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
    async def stop_timer(self, ctx):
        # Команда для остановки таймера
        if self.clean:
            await ctx.channel.purge(limit=1)
        if self.timer:
            self.timer = False
            await ctx.send('Автооповещение остановлено')
        else:
            await ctx.send('Автооповещение не установлено')

    @commands.command(name='toggle_cleaning')
    # @commands.command(name='tc')
    async def clean(self, ctx):
        # Команда для установки автоочистки
        if self.clean:
            await ctx.channel.purge(limit=1)
        if self.clean:
            self.clean = False
            await ctx.send('Автоочистка выключена')
        else:
            self.clean = True
            await ctx.send('Автоочистка включена')

    @commands.command(name='delete_game')
    # @commands.command(name='dg')
    async def delete(self, ctx, game):
        # Команда для удаления игры
        # из списка поддерживаемых игр
        if self.clean:
            await ctx.channel.purge(limit=1)
        try:
            self.find_news.delete_game(int(game))
        except Exception:
            await ctx.send('Ошибка')
        else:
            await ctx.send('Игра удалена')
    

bot = commands.Bot(command_prefix='!')
bot.add_cog(Bot_Commands(bot))
bot.run(TOKEN)
