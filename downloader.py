from bs4 import BeautifulSoup
import requests
import urllib.request
import os.path
import re

class Downloader:

    def __init__(self, session, ügPayload, moodlePayload):
        self.s = session
        self.ügPayload = ügPayload
        self.moodlePayload = moodlePayload

    def download_pdf(self, download_url, path, name):
        name = name.replace(".", " ").replace(":", " ")
        if(name.endswith("pdf")):
            name = list(name)
            name[len(name)-4] = '.'
            name = "".join(name)
        else:
            name = name + ".pdf"
        if(os.path.isfile(os.path.join(path, name))):
            return;
        
        response = self.s.get(download_url)
        file = open(os.path.join(path, name), 'wb')
        file.write(response.content)
        file.close()
        print("Runtergeladen " + name)

    def getTheo1(self, theo1Paths):
        print("Checke Theo1")
        
        loginurl = "http://uebungen.physik.uni-heidelberg.de/uebungen/login.php"
        loginpayload = self.ügPayload
        path = theo1Paths['sheets']
        base = 'https://uebungen.physik.uni-heidelberg.de'
        url = 'https://uebungen.physik.uni-heidelberg.de/uebungen/liste.php?vorl=806'

        self.s.post(loginurl, loginpayload)

        links = BeautifulSoup(self.s.get(url).content, "html.parser").find("ul", {"class": "ulfiles"}).findAll("a")

        for link in links:
            self.download_pdf(base + link.get("href"), path, link.text)

    def getMoodle(self, name, id, paths, scriptDesc, sheetDesc):
        print("Checke %s" % (name))
        
        loginurl = 'https://elearning2.uni-heidelberg.de/login/index.php'
        loginpayload = self.moodlePayload
        url = 'https://elearning2.uni-heidelberg.de/course/view.php?id=%s' % (id)
        scriptPath = paths['scripts']
        excercisePath = paths['sheets']
        miscPath = paths['misc']

        self.s.post(loginurl, loginpayload)

        weeks = BeautifulSoup(self.s.get(url).content, "html.parser").find("ul", {"class": "weeks"}).findAll("div", {"class": "content"})
        weeks.pop(0)
        
        for section in weeks:
            for part in section.findAll("li", {"class": "activity resource modtype_resource "}):
                text = part.find("span", {"class": "instancename"}).text
                if(text == ""):
                    break
                if(text.endswith(" Datei")):
                   text = text[:-6]
                r = self.s.get(part.find("a").get("href"))
                if(text.startswith(scriptDesc)):
                    self.download_pdf(r.url, scriptPath, text)
                elif(text.startswith(sheetDesc)):
                    self.download_pdf(r.url, excercisePath, text)
                else:
                    self.download_pdf(r.url, miscPath, text)
