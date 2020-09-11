from bs4 import BeautifulSoup
import time
import requests
#warto sprawdzić wszystkie polecane i wyświetlić dla użytkownika data-role="suggestion" data-index="2"
#API Allegro kategorie
# żeby poruszać się po stronach
#dodać linki do znalezionych pozycji
#zapis do pliku znalezionych elementów oraz nie powtarzanie wysyłania tego samego elementu
#wykorzystanie podkategori
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.206"}

URL = "https://allegro.pl/listing?string="
URL_SHORT = "https://allegro.pl"
SPACE_URL = "%20"
searchRequest =  "sony nex 5" #str(input())

page = requests.get((URL + searchRequest.replace(" ",SPACE_URL)),headers = headers)

soup = BeautifulSoup(page.content, 'html.parser')

categories = soup.findAll("div", {"data-role":"SuggestedCategories"})
category = list()

for x in soup.find_all("a", {"data-role":"LinkItemAnchor"}):
    temp = x.get_text().strip().split()
    number = ""
    for y in temp:
        if str(y).isdigit():
            number = str(y)
            temp.remove(number)
    category.append((" ".join(temp),number, x['href']))
category.append(("Default",0, URL + searchRequest.replace(" ",SPACE_URL)))

print("\n".join(str(x) for x in category))
URL = URL_SHORT + str(category[int(input())][2])
print(URL)
items = list()

priceLimit = 100

numberOfPages = int(soup.find("span",{"class":"_1h7wt _1fkm6 _g1gnj _3db39_3i0GV _3db39_XEsAE"}).get_text())

for i in range(1,numberOfPages+1,1):
    page = requests.get((URL + "&p=" + str(i)),headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    for x in soup.find_all("div", {"class": "mpof_ki myre_zn _9c44d_1Hxbq"}):
        items.append((x.find("a").get_text(), float(str(x.find("span",{"class" : "_1svub _lf05o"}).get_text())[:-3].replace(",",".").replace(" ",""))))
items.sort(key = lambda x: x[1])
items = list(dict.fromkeys(items))
for x in items:
    print(x[0] + "\nCena: " + str(x[1]))

"""for x in items:
    if x[1] <= priceLimit:
        print("Found good price!")
        print(x[0] + "\nCena: " + str(x[1]))"""
    