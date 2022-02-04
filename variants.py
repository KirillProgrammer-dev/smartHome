# -*- encoding: utf-8 -*-
import random
import re
import requests
from aiohttp import request
from bs4 import BeautifulSoup


class Variants:
    def __init__(self):
        self.weather = ['погода', 'температура']
        self.prepositions = [' в ', ' и ', ' на ', ' около ']
        self.questions = ['какой', 'где', 'почему', 'какая', 'какие']
        self.howAreYouResponses = ['Где-то между хорошо и очень хорошо.', 'После того, как ты спросил, намного лучше.', 'Спасибо, что спросил, ты сделал мой день намного лучше.', 'Лучше, чем у многих людей.', 'Как у тебя, но лучше.', 'Ничего особенного.', 'Не жалуюсь, все равно меня никто не слушает.', 'Достаточно хорошо.', 'Средне, не великолепно, не ужасно, просто средне.', 'Пока все в порядке.']
        self.howAreYou = ['как дела']
        self.Hello = ['привет', 'хай', 'bonjour', 'hi', 'шалом', 'здравствуй', 'салют']
        self.Time = ['время', 'часов']
        self.Wiki = ["что такое"]
        self.offense = ['дура', "дебил"]
        self.answersOffence = ["Кто так обзывается - тот так и называется", "Я так, и обидится могу"]
        self.getStories = ["расскажи сказку", "сказка"]
        self.clothes = ["одеть", "надеть"]
        self.veryCold = ["Сегодня очень холодно, наденьте куртку и теплую обувь", "Сегодня холодно, советую надеть утеплое нижнее бельё"]
        self.warm = ["Сегодня прохладно, советую надеть толстовку и джинсы", ""]

    def getWeather(self):
        return self.weather
    
    def getMatches(self, variants:list, zadanie:str):
        for variant in variants:
            if variant in zadanie:
                return True
        return False
    
    def deletePrepositions(self, zadanie:str):
        for i in self.prepositions:
            zadanie = zadanie.replace(i, '')
        return zadanie
    
    def deleteVariants(self, zadanie:str, variants:list):
        for i in variants:
            zadanie = zadanie.replace(i, '')
        return zadanie
    
    def deleteQuestions(self, zadanie:str):
        for i in self.questions:
            zadanie = zadanie.replace(i, '')
        return zadanie
    
    def prepareWord(self, zadanie:str):
        zadanie = zadanie.strip().replace('ё', 'е').capitalize()
        return zadanie
    
    def responseHowAreYou(self):
        return self.howAreYouResponses[random.randint(0, len(self.howAreYouResponses) - 1)]

    def getHowAreYou(self):
        return self.howAreYou
    
    def responseHello(self):
        return self.Hello[random.randint(0, len(self.Hello) - 1)]
    
    def getHello(self):
        return self.Hello
    
    def getTime(self):
        return self.Time
    
    def getWiki(self):
        return self.Wiki
    
    def yandexAnswer(self, zadanie:str):
        url = "https://www.google.ru/search?q=" + zadanie.strip().replace("зона", "")
        response = requests.get(url)
        response.encoding = "utf-8"
        #soup = BeautifulSoup(response.text, 'lxml')
        #quotes = soup.find_all('tr', class_='BNeawe')
        #if quotes == []: quotes = soup.find_all('div', class_='BNeawe')
        #print(soup.decode('cp1251').encode('utf8'))
        #import json

        #data = json.loads(response.text)
        print(response.json())

    def getOffense(self):
        return self.offense
    
    def answerOffence(self):
        return self.answersOffence[random.randint(0, len(self.answersOffence) - 1)]
    
    def getStory(self):
        url = "https://nukadeti.ru/skazki/dlya_malchikov"
        all_stories_list = []
        all_stories = requests.get(url)
        all_stories.encoding = "utf-8"
        soup_stories = BeautifulSoup(all_stories.text, 'lxml')
        stories = soup_stories.find_all('div', class_='info')
        for story in stories:
            all_stories_list.append(story.a.get('href'))
        
        story_response = requests.get("https://nukadeti.ru" + all_stories_list[random.randint(0, len(all_stories_list) - 1)])
        story_response.encoding = "utf-8"
        soup_story = BeautifulSoup(story_response.text, 'lxml')
        text = soup_story.find_all('div', class_='tale-text')
        string = ""
        for sentence in text[0].p:
            string += sentence
        
        return string

    def answerStory(self):
        return self.getStories
    
    def getClothes(self):
        return self.clothes
    
    def answerClothes(self, weather):
        if weather <= -10:
            return ""

        elif weather <= 0 and weather > -10:
            return ""

        elif weather > 0 and weather <= 10:
            return ""

        elif weather > 10 and weather <= 20:
            return ""

        elif weather > 20 and weather <= 30:
            return ""

        elif weather > 30 and weather <= 40:
            return ""
        
        elif weather > 40:
            return ""
