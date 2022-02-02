# -*- encoding: utf-8 -*-
from pyttsx3 import engine
import speech_recognition as sr
import os
import sys
import webbrowser
import requests
import json
import datetime
from datetime import date
from getMainPartOfWord import Stemmer as getWord
from variants import Variants 
from config import Config

def normalize_city_name(name):
    return name.strip().lower().replace('ё', 'е')


cities = {normalize_city_name(x) for x in open("data/cities.txt", "r").readlines() if x.strip()}
openweatherApiKey = '658a409e6023c63e869f6b066d96bca4'
dictNumbers = {1:'Первое', 2:'Второе', 3:'Третье', 4:'Четвертое', 5:'Пятое', 6:'Шестое', 7:'Седьмое', 8:'Восьмое', 9:'Девятое', 10:'Десятое',
 11:'Одиннадцатое', 12:'Двенадцатое', 13:'Тринадцатое', 14:'Четырнадцатое', 15:'Пятнадцатое', 16:'Шестнадцатое', 17:'Семьнадцатое', 18:'Восемьнадцатое',
 19:'Девятнадцатое', 20:'Двадцатое', 21:'Двадцать первое', 22:'Двадцать второе', 23:'Двадцать третье', 24:'Двадцать четвертое', 25:'Двадцать пятое',
 26:'Двадцать шестое', 27:'Двадцать седьмое', 28:'Двадцать восьмое', 29:'Двадцать девятое', 30:'Тридцатое', 31:'Тридцать первое '}
get_word = getWord()
variants = Variants()
config = Config()

def talk(words):
	try:
		print(words)
		os.system("cd ~")
		os.system(f'bash /home/hacker/speech.sh "{words}"')
	except ValueError:
		pass


def command():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		r.pause_threshold = 1
		r.adjust_for_ambient_noise(source, duration=1)
		audio = r.listen(source)

	try:
		zadanie = r.recognize_google(audio, language="ru-RU").lower()
		print("Вы сказали: " + zadanie)
	except sr.UnknownValueError:
		zadanie = command()
	return zadanie

def makeSomething(zadanie):
	if config.getName() in zadanie:
		zadanie = zadanie.replace(config.getName(), '')
		if 'открыть сайт' in zadanie:
			talk("Уже открываю")
			url = 'https://itproger.com'
			webbrowser.open(url)
		elif 'стоп' in zadanie:
			talk("Да, конечно, без проблем")
			sys.exit()
		elif 'имя' in zadanie:
			talk('Меня зовут ' + (config.getName()).capitalize())
		elif variants.getMatches(variants.getWeather(), zadanie):
			city = None
			for i in cities:
				zadanie = variants.deletePrepositions(zadanie)
				zadanie = variants.deleteVariants(zadanie, variants.getWeather())
				zadanie = variants.deleteQuestions(zadanie)
				zadanie = variants.prepareWord(zadanie)
				if (get_word.stem(variants.prepareWord(i)) == get_word.stem(zadanie)):
					city = i

			if (city != None):
				openweatherApi = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweatherApiKey}&units=metric'
				weatherRequest = requests.get(openweatherApi)
				weatherJson = json.loads(weatherRequest.text)
				weather = weatherJson["main"]["temp"]
				gradus = 'градусов'
				if (abs(int(weather)) % 10 == 1):
					gradus = 'градус'
				elif (abs(int(weather)) % 10 in [2, 3, 4]):
					gradus = 'градуса'
				elif (abs(int(weather)) % 10 in [5, 6, 7, 8, 9, 0]):
					gradus = 'градусов'
				talk(str(round(weather)) + " " + gradus)
			else:
				talk('Я не поняла название города')
		elif 'число' in zadanie and 'какое' in zadanie:
			date = datetime.date.today().day
			talk(dictNumbers[date])
		elif variants.getMatches(variants.getHowAreYou(), zadanie):
			talk(variants.responseHowAreYou())
		
		elif variants.getMatches(variants.getHello(), zadanie):
			talk(variants.responseHello() + '!')


talk('Привет, это твой голосовой помощник ' + (config.getName()).capitalize())

while True:
	makeSomething(command())