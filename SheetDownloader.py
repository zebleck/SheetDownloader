from downloader import Downloader
import requests
import getpass
import os.path
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

name = input("Dein Name: ")

if not(os.path.isfile(name + ".txt")):
    print("""Wilkommen. Dieses Programm wird für dich Skripte und Übungsblätter
für Theoretische Physik 1, Experimentalphysik 1 und Lineare Algebra 1
herunterladen.

Benutzername und Passwort der Übungsgruppenverwaltung/Moodle
werden dafür offensichtlich benötigt. Diese Daten werden in %s.txt
im Ordner dieses Programms gespeichert, um zukünftig schnell
darauf zugreifen zu können (mehr nicht).

Übungsgruppenverwaltung: https://uebungen.physik.uni-heidelberg.de/uebungen/
Moodle: https://elearning2.uni-heidelberg.de/\n""" % (name))
    f = open(name + ".txt", 'w')
    f.write(input("Übungsgruppenverwaltung-Benutzername: ") + "\n")
    f.write(getpass.getpass("Übungsgruppenverwaltung-Passwort: ") + "\n")
    f.write(input("Moodle-Benutzername: ") + "\n")
    f.write(getpass.getpass("Moodle-Passwort: ") + "\n")

    dirPrompts = ['Theo1 Übungsblätter',
                  'Ex1 Skripte', 'Ex1 Übungsblätter', 'Alles andere bezüglich Ex1',
                  'La1 Skripte', 'La1 Übungsblätter', 'Alles andere bezüglich La1']
    
    print("Wähle den Ordner für:")
    for prompt in dirPrompts:
        print("-" + prompt)
        f.write(filedialog.askdirectory(title=prompt) + "\n")
    f.close()

theo1Paths = {"sheets": None}
ex1Paths = {"scripts": None, "sheets": None, "misc": None}
la1Paths = {"scripts": None, "sheets": None, "misc": None}

f = open(name + ".txt", "r")
lines = f.read().splitlines()
f.close()

ügPayload = {'username': lines[0], 'loginpass': lines[1]}
moodlePayload = {'username': lines[2], 'password': lines[3]}
theo1Paths['sheets'] = lines[4]
ex1Paths['scripts'] = lines[5]
ex1Paths['sheets'] = lines[6]
ex1Paths['misc'] = lines[7]
la1Paths['scripts'] = lines[8]
la1Paths['sheets'] = lines[9]
la1Paths['misc'] = lines[10]

s = requests.Session()
dl = Downloader(s, ügPayload, moodlePayload, theo1Paths, ex1Paths, la1Paths)

print("Check beginnt.")
dl.getTheo1()
dl.getEx1()
dl.getLa1()
print("Check beendet.")
