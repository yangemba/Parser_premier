import re
import requests
import bs4
from collections import Counter


result = 0
prem_qnt = 0
act_qnt = 0


def take_info(num='1'):

    response = requests.get('https://premier.ua/zhilaia-nedvizhimost/prodazha-3-komn-kv-?page=' + num)
    b=bs4.BeautifulSoup(response.text, "html.parser")
    html_text= str(b)

    p1 = html_text.split('Обычные')
    p2= str(p1[1]).split('Актуальные')
    text_to_parse = str(p2[0])
    spisok_pars = text_to_parse.split('</div>')
    return text_to_parse


def find_qnt(link):

    response = requests.get(link)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    all =  str(soup).count('<!-- c2 -->')


    premium_find = soup.find('div', 'v-list premium-adv-list')
    if premium_find:
        result = str(premium_find).count('<!-- c2 -->')
        prem_qnt =  result
    else:
        prem_qnt = 0



    actual_find = soup.find('div', 'v-list actual-adv-list')
    if actual_find:
        result = str(actual_find).count('<!-- c2 -->')
        act_qnt = result
    else:
        act_qnt = 0
    '''
    
    ususal_find = soup.find('h3', 'Обычные объявления')
    if ususal_find:
        result = str(ususal_find).count('<!-- c2 -->')
        usual = str(ususal_find)
    else:
        return False
    
    
    #print("Premium: ", find_prem())
    #print("Actual: ", find_actual())
    '''
    usual = all - (act_qnt + prem_qnt)


    page_num = 1

    counter = 0
    return usual, act_qnt, prem_qnt


def statistic(link):
    respons = requests.get(link)
    soupa = bs4.BeautifulSoup(respons.text, "html.parser")
    search_area = soupa.find(id="searchResultContent")
    usual_flag = str(search_area).count('<h3>Обычные объявления</h3>')
    html_text = str(soupa)

    p1 = html_text.split('Обычные')
    p2 = str(p1[0])
    p3 = p2.split('Найдено ')
    p4 = p3[1].split(' объявлен')
    qnt_st_chpt = p4[0]

    if not usual_flag:
        flag_actual = str(search_area).count('actual-adv-list')
        if flag_actual:
            page_num = 1
            KEY_WORD = 'день'
            KEY_WORD_2 = 'дня'
            KEY_WORD_3 = 'дней'
            counter = 0

            while True:
                respons = requests.get(link + '?page=' + str(page_num))
                soupa = bs4.BeautifulSoup(respons.text, "html.parser")
                search_area = soupa.find(id="searchResultContent")
                search_area_without_act = str(search_area).split('actual-adv-list')
                search_area_without_act2 = search_area_without_act[0]
                search2 = search_area_without_act2.findChildren('strong')

                result = str(search2).count(KEY_WORD)
                result2 = str(search2).count(KEY_WORD_2)
                result3 = str(search2).count(KEY_WORD_3)
                lio = str(search_area_without_act2).count('<!-- c2 -->')
                print(result, result2, result3)
                if (result > 0) or (result2 > 0) or (result3 > 0):
                    counter = counter + (lio - (result + result2 + result3))
                    break
                else:
                    counter = counter + lio
                    page_num = page_num + 1
        else:
            page_num = 1
            KEY_WORD = 'день'
            KEY_WORD_2 = 'дня'
            KEY_WORD_3 = 'дней'
            counter = 0
            while True:

                respons = requests.get(link + '?page=' + str(page_num))
                soupa = bs4.BeautifulSoup(respons.text, "html.parser")
                search_area = soupa.find(id="searchResultContent")

                search2 = search_area.findChildren('strong')

                result = str(search2).count(KEY_WORD)
                result2 = str(search2).count(KEY_WORD_2)
                result3 = str(search2).count(KEY_WORD_3)
                lio = str(search_area).count('<!-- c2 -->')
                print(result, result2, result3)
                if (result > 0) or (result2 > 0) or (result3 > 0):
                    counter = counter + (lio - (result + result2 + result3))
                    break
                else:
                    counter = counter + lio
                    page_num = page_num + 1

    else:
        page_num = 1
        KEY_WORD = 'день'
        KEY_WORD_2 = 'дня'
        KEY_WORD_3 = 'дней'
        counter = 0
        while True:
            respons = requests.get(
                link + '?page=' + str(page_num))
            soup = bs4.BeautifulSoup(respons.text, "html.parser")
            red = soup.find(id="searchResultContent")

            selector = red.findChildren('div', class_='v-list')
            right = selector[1]
            lio = str(right).count('<!-- c2 -->')
            search2 = right.findChildren('strong')

            result = str(search2).count(KEY_WORD)
            result2 = str(search2).count(KEY_WORD_2)
            result3 = str(search2).count(KEY_WORD_3)

            print(page_num, result, result2, result3)
            if (result > 0) or (result2 > 0) or (result3 > 0):
                counter = counter + (lio - (result + result2 + result3))
                break
            else:
                counter = counter + lio
                page_num = page_num + 1

    percent = round((counter / int(qnt_st_chpt) * 100), 2)
    return page_num, counter, qnt_st_chpt, percent



#print(find_qnt('https://premier.ua/zhilaia-nedvizhimost/prodazha-3-komn-kv-'))


#print("Usual: ", usual_qnt())

#print([f"https://premier.ua/{x.attrs['href']}" for x in soup.select('.catlist a')])

#print(f"premium is: {find_prem()}, usual is: {find_usual()}, actual: {find_actual()}")







#j = soup.find('div', 'v-list')
#t = str(j)
#k = t.count('день')
