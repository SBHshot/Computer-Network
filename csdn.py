import csv
import os
import tkinter as tk
from tkinter.constants import TRUE, Y
from tkinter.tix import *
from typing import List
import pandas as pd
from pandas.core.frame import DataFrame
# import pygame
import requests
from googleapiclient.discovery import build
from requests.api import request
window = tk.Tk()
window.title('Music Player')
window.geometry('1920x1080')
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side='right', fill=Y)


# YOUTUBE_API_KEY = "AIzaSyAMyDbvjDHp9EJU0p-RnkEQ8hJYDGrZ8tg"
YOUTUBE_API_KEY = "AIzaSyBbnUTrcfhmPHY_YCV1_xs435iz0WzElUk"
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

url = []
title = []
temp = {}
print(type(temp))
music = []
title = []
description = []
img_url = []


def search(query):
    global url, temp, title, description, img_url
    request = youtube.search().list(q=query, part='snippet',
                                    type='music', maxResults=20)
    response = request.execute()
    baseurl = 'https://www.youtube.com/watch?v='
    basechannelurl = 'https://www.youtube.com/channel/'
    # results = response['items'][0]['id']['videoId']
    for index in range(len(response['items'])):
        music = {}
        result1 = response['items'][index]
        df = pd.DataFrame(result1)
        # print(df)
        for key, value in result1['id'].items():
            if(key == 'videoId'):
                isVideo = True
                url.append(baseurl+value)
                title.append(result1['snippet']['title'])
                description.append(result1['snippet']['description'])
                img_url.append(result1['snippet']
                               ['thumbnails']['default']['url'])


def func(name):
    print(name)


# file = pd.read_csv('Result.csv')
if not os.path.isfile('Result.csv'):
    search('Mayday')
    print(len(url))
    print(len(title))
    print(len(description))
    print(len(img_url))
    print(description)
    zipped = zip(url, title, description, img_url)
    data = pd.DataFrame(list(zipped), columns=[
        'url', 'title', 'description', 'img_url'])
    data.to_csv('Result.csv')
else:
    file = pd.read_csv('Result.csv')
    print(file)
    for idx, row in file.iterrows():
        url.append(str(row['url']))
        title.append(str(row['title']))
        description.append(str(row['description']))
        img_url.append(str(row['img_url']))


for a, b, c, d in zip(url, title, description, img_url):
    label = tk.Label(window, text=b)
    button = tk.Button(window, text=a, command=lambda: func(a))
    label.pack()
    button.pack()

window.mainloop()
