import json
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
import requests
from config import keys
from telebot import types
from datetime import datetime

# извлечение данных с файла json
with open('files/380009616/3124/3124.json') as f:
    file_content = f.read()
    templates = json.loads(file_content)

kusp = templates['kusp']
date_kusp = templates['current_datetime']
kusp_info = f'{kusp} от {date_kusp}'
images = templates['images']

# блок работы с шаблоном фототаблицы
doc = docx.Document('files/fototable_sample.docx')#открываю экземпляр шаблона фототаблицы

# получаю объект верхнего колонтитула
header = doc.sections[0].header
title = header.tables[0] # таблица с информацией о КУСП (номер КУСП и дата)
kusp_cell = title.cell(0, 1) # ячейка содержащая информацию о КУСП
kusp_cell.text = kusp_info # текст ячейки содержащей номер КУСП

# Содержание фототаблицы
number_of_rows = len(images)*2 #количество строк в таблице равно количеству фотографий умноженное на 2 (строка с пояснениями)

for row in range(number_of_rows):
    if (row % 2) == 0:
        # Добавляем пустой абзац
        p = doc.add_paragraph()
        # Добавляем пустой прогон
        run = p.add_run()
        run.add_picture(images[row // 2]["name"], width=docx.shared.Cm(12))
        # выравниваем картинку посередине страницы
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # cell.add_picture('files/380009616/3124/file_12.jpg', width=docx.shared.Cm(12))
            # images[row // 2]["name"]
    else:
        # Добавляем абзац с порядковым номером фотографии
        p = doc.add_paragraph(f'Фото №{str(row // 2 + 1)}. ')
        # Добавляем прогон с коментарием к фотографии
        run = p.add_run(images[row // 2]["photo_description"])
        # выравниваем коментарий по ширине страницы
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        # Добавляем пустой абзац для визуального разделения
        doc.add_paragraph()


# сохранение файла в папке с фотографиями под именем КУСП
doc.save('files/380009616/3124/fototable.docx')
