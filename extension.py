import json
import requests
from config import keys
from telebot import types
from datetime import datetime

# Класс исключений, для проверки корректного ввода пользовательского запроса
class APIException(Exception):
    pass

# Основной класс
class CryptoConverter:
    # Метод отслеживающий нажатие кнопок в меню, принимает текс сообщения, возвращает True/Fаlse
    @staticmethod
    def checking_input(input_str: str):# Принимает текст сообщения от пользователя
        pressing_button = False # Показатель срабатывания кнопки - пока не известно сообщение введено вручную или с кнопки
        for i_key, i_value in keys.items(): # Проверяю по словарю валют
            if(i_key + ' / ' + i_value) == input_str: # если строка "Ключ + / + значение" совпадает с текстом сообщения,
                Menu_with_buttons.pressing_button += 1 # то была нажата соответсвующая Ключу кнопка и
                pressing_button = True # показатель срабатывания кнопки в режим True
                if Menu_with_buttons.pressing_button == 1: # Если кнопка из меню сработала первый раз, то
                    Menu_with_buttons.values = [i_key] # ключ соответствует исходной валюте, ставим ее в начало списка и
                    return pressing_button # возвращаем True - сообщение получено при нажатии кнопки
                elif Menu_with_buttons.pressing_button == 2: # Если же кнопка сработала второй раз, то
                    Menu_with_buttons.values.append(i_key)# ключ соответствует результирующей валюте, дополняем список и
                    return pressing_button # возвращаем True - сообщение получено при нажатии кнопки
        if Menu_with_buttons.pressing_button == 2: # Если сообщение отправлено пользователем не путем нажатия одной из кнопок,
            try: # но при этом кнопки срабатывали дважды, возможно пользователь ввел количество исходной валюты
                amount = float(input_str) # переводим сообщение пользователя в число, предворительно улавливая исключение
                Menu_with_buttons.values.append(amount) # число добавляем в список как количество исходной валюты
                Menu_with_buttons.pressing_button = 0 # обнуляем счетчик нажатия кнопок
            except ValueError:
                raise ConnectionError(f'Не верный формат количества валюты {input_str}, введите число')

        return pressing_button # возвращаем False, так как последнее сообщение с количеством исходной валюты, введено в ручную

    # Метод, проверяющий корректность запроса, отправляющий запрос на сервер, обрабатывающий поступивший контент
    @staticmethod
    def get_price(quote: str, base: str, amount: str): # принимает название исходной, результативной валют и количество исходной валюты
        if quote == base: # проверка на совпадение исходной и результативной валют
            raise APIException(f'Исходная и результативная валюты совпадают - {base}')
        try: # присваиваю переменной quote_ticker значение ключа quote - исходная валюта
            quote_ticker = keys[quote]  # ключ - устоявшееся название валюты, значение - официальное международное название
        except KeyError: # если пользователь ввел название одной из валют с ошибкой, то сработает исключение
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base] # присваиваю переменной base_ticker значение ключа base - результирующая валюта
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)# проверка правильности ввода пользователем числа - количества исходной валюты
        except ValueError:
            raise ConnectionError(f'Не верный формат количества валюты {amount}, введите число')
        # Отправляю сформированный запрос API на сервер и получаю ответ в переменную r
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        # из полученного ответа вычленяем стоимость валюты и присваиваем ее к переменной total_base
        total_base = json.loads(r.content)[base_ticker]
        return total_base * amount # возвращаем стоимость валюты, умноженную на количество

# Класс формирующий меню кнопок
class Menu_with_buttons:
    pressing_button = 0 # количество нажатий на кнопки, запрос формируется из двух последовательных нажатий и ручного ввода количества исходной валюты
    values = [] # Список, содержащий элементы запроса - [<Исходная валюта>, <Результирующая валюта>, <Количество исходной валюты>]
    # Метод построения меню
    @staticmethod
    def building_menu(keys):
        button_obj = types.ReplyKeyboardMarkup()
        for i in keys: # Количество кнопок в меню соответствует количеству видов валют
            keys_button = types.KeyboardButton(i) # Создаю кнопку с подписью - "Ключ меню"
            button_obj.add(keys_button) # Добавляю кнопку в меню
        return button_obj # Передаю сформированное меню

# Класс содержащий всю информацию о фототаблице
class Fototable():

    # пункты меню
    FOTOTABLE_MENU = ['1. КУСП', '2. Адрес места происшествия', '3. Должность', '4. Звание', '5. Фамилия и инициалы', '6. Фотография и подпись']
    action_counter = 0  # Счетчик действий по заполнению данных фототаблицы
    kusp = 0 # Номер зарегистрированного события КУСП
    images = [] # Список значения которого пары - изображение, описание
    current_datetime = datetime.now().date() # Текущая дата
    id_user = 0
    job_title = 'УУП'
    rank = 'лейтенант'
    fio = 'Р.Р. Назаров'
    address = 'Московская область, Рузский городской округ,'

    def json(self, patch):
        pass

    def __str__(self):
        return f"id_user: {self.id_user}, kusp: {self.kusp}, current_datetime: {self.current_datetime}, images: {self.images}"

    def display_info(self):
        print(self.__str__())




