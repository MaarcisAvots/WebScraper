import requests
import time
from bs4 import BeautifulSoup as bs
import csv

URL = "http://books.toscrape.com/catalogue"
LAPAS = "lapas/"
DATI = "dati/"

def saglabat(url, datne):
    rezultats = requests.get(url)
    if rezultats.status_code == 200:
        with open(f"{LAPAS}{datne}", 'w', encoding='UTF-8') as f:
            f.write(rezultats.text)
    else:
        print(f"ERROR: Statusa kods {rezultats.status_code}")


def lejupieladet_lapas(cik):
    for i in range(1, cik + 1):
        saglabat(f"{URL}/page-{i}.html", f"{i}_lapa.html")
        time.sleep(1)

def info(datne):
    dati = []
    with open(datne, 'r', encoding='UTF-8') as f:
        html = f.read()

    base = bs(html, "html.parser")

    galvena = base.find_all("article", class_="product_pod")
    

    #print(galvena)
    # for i in range(1, len(galvena)):
    #     print("==========================")
    #     print(i, galvena[i].get_text())
    # print("==========================")

    for row in galvena:
        gramata = {}
        # print(row)
        #print("=======================")
        tags = row.find('h3')
        gramata['nosaukums'] = tags.find('a')['title']
        #print("Nosaukums: "+gramata['nosaukums'])



        gramata['vertejums'] = row.find('p')['class']
        gramata['vertejums'] =str(gramata['vertejums'])
        size = len(gramata['vertejums'])
        gramata['vertejums'] = gramata['vertejums'][17:size - 2]
        #print("Vērtējums: "+gramata['vertejums'])


        tags = row.find('p', class_="price_color")
        gramata['cena'] = tags.find
        gramata['cena'] =str(gramata['cena'])
        size = len(gramata['cena'])
        gramata['cena'] = gramata['cena'][50:size - 5]
        #print("Cena: "+gramata['cena'])


        tags = row.find('p', class_="instock availability")
        gramata['vaiir'] = tags.find
        gramata['vaiir'] =str(gramata['vaiir'])
        size = len(gramata['vaiir'])
        gramata['vaiir'] = gramata['vaiir'][96:size -11]
        #print("Vai ir pieejams: "+gramata['vaiir'])

        dati.append(gramata)
    return dati

def saglabat_datus(dati):
    with open(f"{DATI}gramatas.csv", 'w', encoding='UTF-8', newline="") as f:
        kolonu_nosaukumi = ['nosaukums', 'vertejums', 'cena', 'vaiir']
        w = csv.DictWriter(f, fieldnames= kolonu_nosaukumi)
        w.writeheader()
        for gramata in dati:
            w.writerow(gramata)


cik = 50
#lejupieladet_lapas(cik)
def izvilkt_datus(cik):
    visi_dati = []
    for i in range(1, cik + 1):
        datne = f"{LAPAS}{i}_lapa.html"
        datnes_dati = info(datne)
        visi_dati += datnes_dati

    saglabat_datus(visi_dati)
izvilkt_datus(cik)