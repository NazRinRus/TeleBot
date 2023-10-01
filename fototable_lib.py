import json
import docx
import requests
from config import keys
from telebot import types
from datetime import datetime

kusp = '4560'
date_kusp = '01.10.2023'
kusp_info = f'{kusp} от {date_kusp}'
images = [
    {"name": "files/380009616/3124/file_11.jpg", "photo_description": "\u0421\u0447\u0435\u0442\u0447\u0438\u043a"},
    {"name": "files/380009616/3124/file_12.jpg", "photo_description": "\u0421\u0447\u0451\u0442\u0447\u0438\u043a \u0441\u043d\u0442 \u0436\u0435\u043b\u0435\u0437\u043d\u043e\u0434\u043e\u0440\u043e\u0436\u043d\u0438\u043a"}
]

# блок работы с шаблоном фототаблицы
doc = docx.Document('files/fototable_sample.docx')#открываю экземпляр шаблона фототаблицы

# получаю объект верхнего колонтитула
header = doc.sections[0].header
title = header.tables[0] # таблица с информацией о КУСП (номер КУСП и дата)
kusp_cell = title.cell(0, 1) # ячейка содержащая информацию о КУСП
kusp_cell.text = kusp_info # текст ячейки содержащей номер КУСП

# Содержание фототаблицы
number_of_rows = len(images)*2 #количество строк в таблице равно количеству фотографий умноженное на 2 (строка с пояснениями)
table1 = doc.add_table(rows=number_of_rows, cols=1) # построение объекта таблицы
# заполнение таблицы данными
for row in range(number_of_rows):
    cell = table1.cell(row, 0)
    if (row % 2) == 0:
        cell.text = images[row // 2]["name"]
    else:
        cell.text = images[row // 2]["photo_description"]


# сохранение файла в папке с фотографиями под именем КУСП
doc.save('files/380009616/3124/fototable.docx')
