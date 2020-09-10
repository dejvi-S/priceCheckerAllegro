from bs4 import BeautifulSoup
import time
import requests
#_d25db_3Rp9D - class controls visibility os sugestions
#mgmw_vr - klasa 1 usunać w kategorii
#mgmw_s9 - klasa 2
#warto sprawdzić wszystkie polecane i wyświetlić dla użytkownika data-role="suggestion" data-index="2"
#API Allegro kategorie
# żeby poruszać się po stronach
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.206"}

URL = "https://allegro.pl/listing?string="
SPACE_URL = "%20"
searchRequest =  "aparat bezlusterkowiec Sony nex 5" #str(input())

page = requests.get((URL + searchRequest.replace(" ",SPACE_URL)),headers = headers)

soup = BeautifulSoup(page.content, 'html.parser')

items = list()

priceLimit = 100

numberOfPages = int(soup.find("span",{"class":"_1h7wt _1fkm6 _g1gnj _3db39_3i0GV _3db39_XEsAE"}).get_text())

for i in range(1,numberOfPages+1,1):
    page = requests.get((URL + searchRequest.replace(" ",SPACE_URL) + "&p=" + str(i)),headers = headers)
    for x in soup.find_all("div", {"class": "mpof_ki myre_zn _9c44d_1Hxbq"}):
        items.append((x.find("a").get_text(), float(str(x.find("span",{"class" : "_1svub _lf05o"}).get_text())[:-3].replace(",","."))))
items.sort(key = lambda x: x[1])
for x in items:
    print(x[0] + "\nCena: " + str(x[1]))

for x in items:
    if x[1] <= priceLimit:
        print("Found good price!")
        print(x[0] + "\nCena: " + str(x[1]))
    