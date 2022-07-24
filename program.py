import requests
from bs4 import BeautifulSoup

program = requests.get("https://tv.mail.ru/moskva/")
program_parsed = BeautifulSoup(program.text, "lxml")
print(program.text)
program_class = program_parsed.find_all("a", class_="p-channels__item__info__title__link")
all_program_list = []
for i in program_class:
    all_program_list.append(i.text)

print(all_program_list)

with open("data/programms.txt", "a+", encoding="utf-8") as f:
    for i in all_program_list:
        f.write(i + "\n")