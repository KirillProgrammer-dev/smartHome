import random


class Variants:
    def __init__(self):
        self.weather = ['погода', 'температура']
        self.prepositions = [' в ', ' и ', ' на ', ' около ']
        self.questions = ['какой', 'где', 'почему', 'какая', 'какие']
        self.howAreYouResponses = ['Где-то между хорошо и очень хорошо.', 'После того, как ты спросил, намного лучше.', 'Спасибо, что спросил, ты сделал мой день намного лучше.', 'Лучше, чем у многих людей.', 'Как у тебя, но лучше.', 'Ничего особенного.', 'Не жалуюсь, все равно меня никто не слушает.', 'Достаточно хорошо.', 'Средне, не великолепно, не ужасно, просто средне.', 'Пока все в порядке.']
        self.howAreYou = ['как дела']
        self.Hello = ['привет', 'хай', 'bonjour', 'hi', 'шалом', 'здравствуй', 'салют']

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