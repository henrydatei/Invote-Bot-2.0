import requests
from lxml import html
import random
import argparse

parser = argparse.ArgumentParser(description='Gib mir eine Umfrage-ID!')
parser.add_argument("--id")
args = parser.parse_args()
id = int(args.id)

seed = random.randint(1,10000)

page = requests.get("https://invote.tu-dresden.de/{}".format(str(id)))
tree = html.fromstring(page.content)

frage = tree.xpath('/html/body/div[1]/div[2]/div/div[1]/form/div/div/div/p/strong/text()')[0][5:-5][4:]
print(frage)

anzahlAntworten = len(tree.find_class("antwort"))
antworten = [None] * anzahlAntworten
for i in range(1,anzahlAntworten+1):
    antworten[i-1] = tree.xpath("/html/body/div[1]/div[2]/div/div[1]/form/div/div/p[{}]/label/text()".format(i))[0][1:]
    print("{}. {}".format(str(i),antworten[i-1]))

antwortIDs = list(map(int,tree.xpath("//*[@name='antwort']/@value")))

print("Welche Antwort soll geschickt werden?")
answer = input()
gesendeteAntwort = antwortIDs[int(answer) - 1]
print("")

print("Wie oft soll Antwort {} geschickt werden?".format(answer))
anzahlString = input()
anzahlInt = int(anzahlString)

#print(antworten)
print(antwortIDs)

for zaehler in range(1,anzahlInt+1):
    requests.post("https://invote.tu-dresden.de/{}".format(str(id)), cookies=dict(invoteSession="{}".format(str(seed + zaehler)),invote="{}".format(str(seed + zaehler))), data={'antwort':"{}".format(str(gesendeteAntwort))})
    print("Fake-Antwort Nummer {} wurde abgeschickt!".format(str(zaehler)))
