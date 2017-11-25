from downloader import Downloader
from inputter import Inputter
import requests
import getpass
import os.path
import tkinter as tk
from tkinter import filedialog

name = Inputter().GetInput()

ex1Id =16267
la1Id = 15818
ana1Id = 16107
theo1Paths = None
ex1Paths = None
la1Paths = None
ana1Paths = None

f = open(name + ".txt", "r")
lines = f.read().splitlines()
f.close()

doesAna = (lines[4] == "y")

ügPayload = {'username': lines[0], 'loginpass': lines[1]}
moodlePayload = {'username': lines[2], 'password': lines[3]}
theo1Paths = {"scripts": None, "sheets": lines[5], "misc": None}
ex1Paths = {"scripts": lines[6], "sheets": lines[7], "misc": lines[8]}
la1Paths = {"scripts": lines[9], "sheets": lines[10], "misc": lines[11]}
if(doesAna):
    ana1Paths = {"scripts": lines[12], "sheets": lines[13], "misc": lines[14]}

s = requests.Session()
dl = Downloader(s, ügPayload, moodlePayload)

print("Check beginnt.")
dl.getTheo1(theo1Paths)
dl.getMoodle("Ex1", ex1Id, ex1Paths, "Vorlesung", "Blatt")
dl.getMoodle("La1", la1Id, la1Paths, "VL", "Übungsblatt")
if doesAna:
    dl.getMoodle("Ana1", ana1Id, ana1Paths, "Vorlesung", "Blatt")
print("Check beendet.")
input("Drücke ENTER Taste zum Beenden ...")
