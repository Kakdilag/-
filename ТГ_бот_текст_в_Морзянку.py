import telebot
from pydub import AudioSegment
from pydub.generators import Sine
import time

# словарь с символами азбуки морзе
slmorz = {'1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
          '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
          'А': '.-', 'Б': '-...', 'В': '.--', 'Г': '--.', 'Д': '-..', 'Е': '.',
          'Ж': '...-', 'З': '--..', 'И': '..', 'Й': '.---', 'К': '-.-',
          'Л': '.-..', 'М': '--', 'Н': '-.', 'О': '---', 'П': '.--.', 'Р': '.-.',
          'С': '...', 'Т': '-', 'У': '..-', 'Ф': '..-.', 'Х': '....',
          'Ц': '-.-.', 'Ч': '---.', 'Ш': '----', 'Щ': '--.-', 'Ъ': '.--.-.',
          'Ы': '-.--', 'Ь': '-..-', 'Э': '...-...', 'Ю': '..--', 'Я': '.-.-'}

# функция для преобразования сообщения в азбуку морзе
def premorz(sabj):
    morz = ""
    for i in sabj:
        if i != " ":
            morz += slmorz[i.upper()] + " "
        else:
            morz += " "
    return morz

# функция для сохранения аудиофайла
def zvumor(morz, imfaj):
    dlito = 50 # длительность точки в миллисекундах
    dlitir = dlito * 3 # длительность тире в миллисекундах
    dliprob = dlito # длительность пробела в миллисекундах
    chasigdec = 440 # частота сигнала в герцах
    zvudec = -20 # громкость сигнала в децибелах

    # создаем объект AudioSegment для хранения аудио данных
    audio_data = AudioSegment.empty()
    for i in morz:
        if i == '.':
            # создаем объект Sine для генерации сигнала с частотой chasigdec и длительностью dlito миллисекунд
            sine_wave = Sine(chasigdec).to_audio_segment(duration=dlito)
            # уменьшаем громкость сигнала на zvudec децибелов
            sine_wave = sine_wave - zvudec
            # добавляем сигнал в общий объект AudioSegment
            audio_data += sine_wave
            # добавляем паузу между символами
            audio_data += AudioSegment.silent(duration=dliprob)
        elif i == '-':
            # создаем объект Sine для генерации сигнала с частотой chasigdec и длительностью dlitir миллисекунд
            sine_wave = Sine(chasigdec).to_audio_segment(duration=dlitir)
            # уменьшаем громкость сигнала на zvudec децибелов
            sine_wave = sine_wave - zvudec
            # добавляем сигнал в общий объект AudioSegment
            audio_data += sine_wave
            # добавляем паузу между символами
            audio_data += AudioSegment.silent(duration=dliprob)
        elif i == ' ':
            # добавляем паузу между словами
            audio_data += AudioSegment.silent(duration=dliprob * 7)
    # сохраняем аудио данные в файл
    audio_data.export(imfaj, format="wav")

#СОЗДАЕМ БОТА
bot=telebot.TeleBot('сюда вводим апи бота') #создаем бота

@bot.message_handler(commands=['start']) #обработчик команды start
def sta(message):
    bot.send_message(message.chat.id, 'Я бот для преобразования текста в Морзянку + высылаю аудиосообщение Морзянки.\n\n Сделал @leshyj')

@bot.message_handler(content_types=['text']) #получение сообщения
def echo(message):
    try:
        sabj = message.text
        sabj = sabj.replace('.', ' ')
        sabj = sabj.replace(',', ' ')
        sabj = sabj.replace('-', ' ')
        sabj = sabj.replace('/', ' ')
        sabj = sabj.replace(':', ' ')
        sabj = sabj.replace('!', ' ')
        sabj = sabj.replace('$', ' ')
        sabj = sabj.replace('#', ' ')
        sabj = sabj.replace(';', ' ')
        sabj = sabj.replace('"', ' ')
        sabj = sabj.replace("'", ' ')
        sabj = sabj.replace('%', ' ')
        sabj = sabj.replace('|', ' ')
        sabj = sabj.upper() #делаем все буквы большими
        morz = premorz(sabj)
        bot.send_message(message.chat.id, text=morz)
        imfaj = 'Голосовое сообщение'
        zvumor(morz, imfaj)
        with open('Голосовое сообщение', 'rb') as f:
            bot.send_voice(message.chat.id, f)
    except:
        bot.send_message(message.chat.id, text=f"Извини, но произошла какая-то дичь") #вывод сообщения если не ок
bot.polling(non_stop = True)
