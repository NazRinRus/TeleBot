import telebot, json
from config import TOKEN, keys
from extension import CryptoConverter, APIException, Menu_with_buttons, Fototable, FototableDataProcessor
from pathlib import Path

bot = telebot.TeleBot(TOKEN)

# Обрабатываются команды 'start', 'help'
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате: \n <название валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты> \n \
    напирмер: биткоин доллар 3 \n \
    или воспользуйтесь меню, введя команду /menu \n \
    Чтобы увидеть список доступных валют, введите команду /values'
    bot.reply_to(message, text)

# Обрабатывается команда 'menu', если пользователь предпочел сформировать запрос кнопками, а не ручным вводом
@bot.message_handler(commands=['menu'])
def menu(message: telebot.types.Message):
    menu1 = Menu_with_buttons.building_menu(keys) # Формируем меню из кнопок
    bot.send_message(message.chat.id, 'Выберите пункт меню', reply_markup=menu1)

# Обрабатывается команда 'values', список доступных валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

# Обрабатывается поступление текстового сообщения
@bot.message_handler(content_types=['text', 'photo'])
def convert(message: telebot.types.Message):
    fototable = Fototable
    if message.text == '1. Фототаблица':
        fototable.action_counter = 1 # первый этап заполнения данных фототаблицы
        bot.send_message(message.chat.id, 'Введите номер КУСП (при его отсутствии введите 0)')
    elif fototable.action_counter == 1:
        fototable.action_counter = 2 # второй этап заполнения данных фототаблицы
        fototable.kusp = int(message.text)
        print(fototable.kusp)
        print(message.from_user.id)
        bot.send_message(message.chat.id, 'Выберите изображение и подпись к нему')
    elif (fototable.action_counter == 2)and(message.content_type == 'photo'):
        Path(f'files/{message.chat.id}/{fototable.kusp}/').mkdir(parents=True, exist_ok=True)
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        photo_description = message.caption
        print(photo_description)
        src = f'files/{message.chat.id}/{fototable.kusp}/' + file_info.file_path.replace('photos/', '')
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        imag = {'name':src, 'photo_description':photo_description}
        fototable.images.append(imag)
        fototable.id_user = message.from_user.id
        bot.send_message(message.chat.id, 'Фотография загружена')
# Тестирование, далее заменить "тест" на команду окончания формирования фототаблицы
    elif message.text == 'тест':
        str1 = fototable()
        print(str1)
        # формирование json файла
        patch = f'files/{message.chat.id}/{fototable.kusp}/'
        print(patch)
        json1 = FototableDataProcessor(fototable.id_user, fototable.kusp, fototable.current_datetime, fototable.images, patch)
        json1.fototable_json_save()
        bot.send_message(message.chat.id, str1)


        # menu_fototable = Menu_with_buttons.building_menu(fototable.FOTOTABLE_MENU)  # Формируем меню из кнопок
        # bot.send_message(message.chat.id,'Заполните данные', reply_markup=menu_fototable)
    # Так как реакцией нажатия кнопки является отправка сообщения, содержащего название кнопки,
    #pressing_button = CryptoConverter.checking_input(message.text)# проверяем соответствует ли текст названию одной из кнопок
    # if Menu_with_buttons.pressing_button == 0: # Если количество срабатывания кнопок = 0,
    #     if len(Menu_with_buttons.values) == 3: # и если список элементов запроса состоит из трех элементов, то
    #         values = Menu_with_buttons.values # запрос сформирован при помощи кнопок, передаем его в обработку, а
    #         Menu_with_buttons.values = [] # список с элементами запроса класса Меню очищаем
    #     else: # Иначе, если кнопки не срабатывали, и список элементов запроса класса Меню не полный, то возможно
    #         values = message.text.split(' ') # пользователь ввел запрос вручную, разбиваем его на список запроса
    #     try:
    #         if len(values) != 3: # если в списке запроса не достаточно элементов или их больше, то обрабатываем исключение
    #             raise APIException(
    #                 'Параметров должно быть три: <название валюты>, <в какую валюту перевести>, <количество переводимой валюты>')
    #         # Достаем из списка запроса элементы <Исходная валюта>, <Результирующая валюта>, <Количество исходной валюты> и
    #         quote, base, amount = values # присвоим их к переменным, которые далее передаем в качестве атрибутов
    #         total_base = CryptoConverter.get_price(quote, base, amount) # получаем стоимость валюты
    #     except APIException as e:
    #         bot.reply_to(message, f'Ошибка пользователя. \n {e}')
    #     except Exception as e:
    #         bot.reply_to(message, f'Не удалось обратобать команду \n {e}')
    #     else:
    #         text = f'Цена {amount} {quote} в {base} - {total_base}' # Формируем ответ
    #         bot.send_message(message.chat.id, text) # Высылаем ответ


bot.polling(none_stop=True)