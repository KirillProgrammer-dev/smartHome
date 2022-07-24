# -*- encoding: utf-8 -*-
from numpy import var
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
import wikipedia 
import re
import socket
import bluetooth


user_ip = socket.gethostbyname(socket.gethostname())
print(user_ip)
wikipedia.set_lang("ru") 

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

def talk(words): #function to synthesize human-like speech
	try:
		print(words)
		os.system("cd ~")
		os.system(f'bash speech.sh "{words}"')
	except ValueError:
		print("Error")


def getWeather(zadanie, user_ip, cities):
	city = None
	for i in cities:
		zadanie = variants.deletePrepositions(zadanie)
		zadanie = variants.deleteVariants(zadanie, variants.getWeather())
		zadanie = variants.deleteQuestions(zadanie)
		zadanie = variants.prepareWord(zadanie)
		#print(zadanie)
		if (get_word.stem(variants.prepareWord(i)) == get_word.stem(zadanie)):
			city = i
	if city == None:
		url = f"https://ip-geo-location.p.rapidapi.com/ip/{user_ip}"

		querystring = {"format":"json"}

		headers = {
			'x-rapidapi-host': "ip-geo-location.p.rapidapi.com",
			'x-rapidapi-key': "cdbf458776msh6db1411cfa434cap1da535jsncb6d50067b80"
			}

		response = requests.request("GET", url, headers=headers, params=querystring)
		print(response)

	if (city != None):
		print(city)
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
		return (str(round(weather)) + " " + gradus, weather)
	else:
		return ('Я не поняла название города', None)

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

def makeSomething(zadanie): #main fuction to process sentensec and answer
	answers = 0
	if config.getName() in zadanie:
		zadanie = zadanie.replace(config.getName(), '')
		if 'открыть сайт' in zadanie:
			talk("Уже открываю")
			url = 'https://itproger.com'
			answers = 1
			webbrowser.open(url)

		elif 'стоп' in zadanie:
			talk("Да, конечно, без проблем")
			sys.exit()
			answers = 1

		elif 'имя' in zadanie:
			talk('Меня зовут ' + (config.getName()).capitalize())

		elif variants.getMatches(variants.getWeather(), zadanie):
			talk(getWeather(zadanie, user_ip, cities)[0])
			answers = 1
		
		elif variants.getMatches(variants.getClothes(), zadanie):
			talk(variants.answerClothes(getWeather(zadanie, user_ip)[1]))
			answers = 1

		elif 'число' in zadanie and 'какое' in zadanie:
			date = datetime.date.today().day
			talk(dictNumbers[date])
			answers = 1

		elif variants.getMatches(variants.getHowAreYou(), zadanie):
			talk(variants.responseHowAreYou())
			answers = 1
		
		# elif variants.getMatches(variants.getHowAreYou(), zadanie):
		# 	talk(variants.responseHowAreYou())
		# 	answers = 1
		
		elif variants.getMatches(variants.getOffense(), zadanie):
			talk(variants.answerOffence())
			answers = 1

		elif variants.getMatches(variants.answerStory(), zadanie):
			talk("Хорошо")
			talk(variants.getStory())
			answers = 1

		elif variants.getMatches(variants.getCook(), zadanie):
			talk(variants.answerCook())
			answers = 1
		
		elif variants.getMatches(variants.getPlus(), zadanie):
			talk(variants.answerPlus(zadanie))
			answers = 1
			
		elif variants.getMatches(variants.getMinus(), zadanie):
			talk(variants.answerMinus(zadanie))
			answers = 1
			
		elif variants.getMatches(variants.getMultiplication(), zadanie):
			talk(variants.answerMultiplication(zadanie))
			answers = 1
			
		elif variants.getMatches(variants.getMultiplication(), zadanie):
			talk(variants.answerMultiplication(zadanie))
			answers = 1
			
		elif variants.getMatches(variants.getDevide(), zadanie):
			talk(variants.answerDevide(zadanie))
			answers = 1
		
		elif variants.getMatches(variants.getJoke(), zadanie):
			talk(variants.answerJoke())
			answers = 1

		elif variants.getMatches(variants.getProgram(), zadanie):
			talk(variants.answerProgram())
			answers = 1

		elif "включ" in zadanie and "свет" in zadanie:
			sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
			sock.connect(("3C:71:BF:F9:69:4E", 1))
			sock.send("0")
			sock.close()
			talk("Хорошо, сделано")
		
		elif "выключ" in zadanie and "свет" in zadanie:
			sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
			sock.connect(("3C:71:BF:F9:69:4E", 1))
			sock.send("1")
			sock.close()
			talk("Хорошо, сделано")

		elif not answers:
			try:
				if wikipedia.page(variants.deleteVariants(str(zadanie).replace("зона", ""), variants.getWiki())):
					talk(re.sub(r"\(.+?\)\s", "", wikipedia.page(variants.deleteVariants(str(zadanie).replace("зона", ""), variants.getWiki())).content).replace("«", "").replace("»", "").split(".")[0])
			except wikipedia.exceptions.DisambiguationError:
				talk("К сожелению я не могу выполнить данное задание")			
			except wikipedia.exceptions.PageError: 
				talk("К сожелению я не могу выполнить данное задание")
		#elif variants.getMatches(variants.getWiki(), zadanie):
		#	talk(re.sub(r"\(.+?\)\s", "", wikipedia.page(variants.deleteVariants(zadanie, variants.getWiki())).content).replace("«", "").replace("»", "").split(".")[0])
		

		#elif variants.yandexAnswer(zadanie):
		#	talk(variants.yandexAnswer(zadanie)[0])
talk('Привет, это твой голосовой помощник ' + (config.getName()).capitalize())

while True:
	makeSomething(command())