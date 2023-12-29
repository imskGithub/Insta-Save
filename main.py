import datetime
import json
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

    history = {}
    if not os.path.exists("history.json"):
        for i in dump.split(sep):
            Instagram_Save(i, date)
            history[str(i)] = str(date)
    else:
        with open("history.json", "r") as file:
            history = json.load(file)

        for i in dump.split(sep):
            if not (str(i) in history):
                Instagram_Save(i, date)
                history[str(i)] = str(date)
            else:
                history_date = str(history[str(i)])
                if not os.path.exists(history_date):
                    Instagram_Save(i, date)
                    history[str(i)] = str(date)
                else:
                    if not os.path.exists(f"{history_date}/{str(i)}.jpg"):
                        Instagram_Save(i, date)
                        history[str(i)] = str(date)
                    else:
                        with open(f"{history_date}/{str(i)}.jpg", "rb") as file:
                            history_image = file.read()
                        link = getImageLink(i)
                        r = requests.get(link)
                        if history_image == r.content:
                            pass
                        else:
                            writeImage(link, i, date)
                            history[str(i)] = date

    with open("history.json", "w") as file:
        json.dump(history, file)


if not os.path.exists(date):
    os.makedirs(date)

# Example - Instagram_Save("youtube")
# Example - Instagram_Saves(filename="list.txt", sep="\n")


# Write your code above this!
if not os.listdir(date):
    os.rmdir(date)
