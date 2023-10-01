import json
import docx
import requests
from config import keys
from telebot import types
from datetime import datetime

doc = docx.Document('files/fototable_sample.docx')

paragraph1 = doc.add_paragraph('Это первый абзац')
paragraph2 = doc.add_paragraph('Это второй абзац')

paragraph1.add_run('этот текст добавлен в первый абзац')
paragraph2.add_run('этот текст добавлен во сторой абзац')

doc.save('files/380009616/3124/fototable.docx')
