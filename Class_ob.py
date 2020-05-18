import re
import requests
import bs4
from collections import Counter
import find_qnt_ads
import datetime

with open("Parse_list.txt", 'r') as file:
    file.seek(0)
    text = file.read().replace(' ', '')
    LIST_TO_PARSE = text.split(',')

today = datetime.date.today()
with open(f'{str(today)}.csv', 'w') as file:
    file.seek(0)


class ProhodRazdel:
    Url = None
    list_names2 = []

    def get_lin_list(self):
        response = requests.get(self.Url)
        self.soup = bs4.BeautifulSoup(response.text, "html.parser")
        #self.name_area = self.soup.find(id="CategoryHeader120")
        #self.name = self.soup.find(id='headerItema')
        self.list = [f"https://premier.ua/{x.attrs['href']}" for x in self.soup.select('.catlist a')]
        self.list_names = [f"{x.attrs['title']}" for x in self.soup.select('.catlist a')]

        for x in self.list_names:
            k = x.replace(',',' ')
            self.list_names2.append(k)
        dict_linksname = dict(zip(self.list[1:], self.list_names2[1:]))
        return dict_linksname #self.name


def pars_razdel(link):
    proh = ProhodRazdel()
    proh.Url = link
    return proh.get_lin_list()


def prog(list):
    parsed = []
    for key in list:
        try:
            k = find_qnt_ads.find_qnt(key)
            j = find_qnt_ads.statistic(key)
            parsed.append(key + ',' + list[key] + f", {j[0]} стр, {j[1]} из {j[2]}, {j[3]} %, usual : {k[0]}-actual :{k[1]}-premium : {k[2]} \n***\n ")
        except Exception as ex:
            parsed.append(f"error {ex}\n***\n")

    return parsed


def parse(list_to_parse):
    for element in list_to_parse:
        with open(f'{str(today)}.csv', 'a') as file:
            file.seek(0)
            file.write('Ссылка, раздел, Страниц за сегодня, объектов сегодня(обчных)/всего, % заполнения рубрики, обычных-актуальных-премиум \n')
            file.writelines(prog(pars_razdel(element)))
            file.write('\n\n*******************************\n******************************\n******************************\n\n')


parse(LIST_TO_PARSE)
