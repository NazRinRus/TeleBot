import json
import requests
from config import keys
from telebot import types
from datetime import datetime

# Класс исключений, для проверки корректного ввода пользовательского запроса
class APIException(Exception):
    pass

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
class Fototable:

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

    def __str__(self):
        return f"id_user: {self.id_user}, kusp: {self.kusp}, current_datetime: {self.current_datetime}, images: {self.images}"

    def display_info(self):
        print(self.__str__())


# Класс обрабатывающий данные Фототаблицы
class FototableDataProcessor:
    def __init__(self, id_user, kusp, current_datetime, images, patch):
        self.id_user = id_user
        self.kusp = kusp
        self.current_datetime = current_datetime
        self.images = images
        self.patch = patch

    def fototable_json_save(self):
        to_json = {'id_user': self.id_user, 'kusp': self.kusp, 'current_datetime': str(self.current_datetime), 'images': self.images}
        print(to_json)
        with open(f"{self.patch}{self.kusp}.json", 'w') as f:
            json.dump(to_json, f)



