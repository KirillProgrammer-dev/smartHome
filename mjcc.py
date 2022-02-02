import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
class mjcc:
    def __init__(self):
        self.path = "https://mjcc.ru/"
    
    def getStart(self):
        response = requests.get(self.path)
        if response.status_code == 200:
            return response.text
    
    def parseBs4(self):
        soup = BeautifulSoup(self.getStart(), 'lxml')
        date = str(soup.findAll('a', href="/zazhiganiya/")[1].span.text).split()
        time = date[2]
        day = int(date[0])
        datetimeDate = datetime.datetime(int(datetime.date.today().year), int(datetime.date.today().month), day, int(time.split(':')[0]), int(time.split(':')[1]))
    
    
        


mjcc().parseBs4()