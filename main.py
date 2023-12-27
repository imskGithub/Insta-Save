import datetime
import requests
import os
from bs4 import BeautifulSoup as bs


def getImageLink(username):
    r = requests.get(f"https://www.instagram.com/{username}")
    soup = bs(r.text, "html.parser")
    tag = soup.find("meta", attrs={"property": "og:image"})
    link = tag["content"]
    return link


def writeImage(link, filename, date):
    r = requests.get(link, stream=True)
    with open(f"{str(date)}/{filename}.jpg", "wb") as file:
        file.write(r.content)


def getDate():
    dateObj = datetime.datetime.now()
    date = f"{dateObj.strftime('%d')}-{dateObj.strftime('%m')}-{dateObj.strftime('%Y')}"
    return date


date = getDate()


def Instagram_Save(username, date=date):
    writeImage(getImageLink(username), username, date)


def Instagram_Saves(filename="list.txt", date=date, sep="\n"):
    with open(f"{filename}", "r") as file:
        dump = file.read()
    for i in dump.split(sep):
        Instagram_Save(i, date)


if not os.path.exists(date):
    os.makedirs(date)

# Example - Instagram_Save("youtube")
# Example - Instagram_Saves(filename="list.txt", sep="\n")
