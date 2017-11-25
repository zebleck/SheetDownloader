import tkinter as tk
from tkinter import filedialog
import getpass
import os.path

class Inputter:
    def GetInput(self):
        root = tk.Tk()
        root.withdraw()
        
        name = input("Dein Name: ")

        if not(os.path.isfile(name + ".txt")):
            self.Setup(name)
        return name

    def Setup(self, name):
        print("""Wilkommen. Dieses Programm wird für dich Skripte und Übungsblätter
für Theoretische Physik 1, Experimentalphysik 1, Lineare Algebra 1 oder Analysis 1
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
        doesAna = self.GetYesNo("Nimmst du an Analysis 1 teil [Y/N]? ")
        f.write(doesAna + "\n")
    
        dirPrompts = ['Theo1 Übungsblätter',
                        'Ex1 Skripte', 'Ex1 Übungsblätter', 'Alles andere bezüglich Ex1',
                        'La1 Skripte', 'La1 Übungsblätter', 'Alles andere bezüglich La1']
        anaPrompts = ['Ana1 Skripte', 'Ana1 Übungsblätter', 'Alles andere bezüglich Ana1']
                    
        print("Wähle den Ordner für:")
        for prompt in dirPrompts:
            print("-" + prompt)
            f.write(filedialog.askdirectory(title=prompt) + "\n")
        if doesAna == "y":
            for prompt in anaPrompts:
                print("-" + prompt)
                f.write(filedialog.askdirectory(title=prompt) + "\n")
        else:
            for i in range(3):
                f.write("-\n")
        f.close()

    def GetYesNo(self, question):
        while True:
            answer = input(question)
            if answer.lower() == 'y' or answer.lower() == 'n':
                return answer.lower()
            
