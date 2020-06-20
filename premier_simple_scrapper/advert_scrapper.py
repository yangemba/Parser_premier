import lxml
from lxml.etree import Element
from lxml import etree
import logging
from lxml import html
import requests
import bs4

from utils.const import PAGE_INDICATOR, DATA_OFF_WORD_1, DATA_OFF_WORD_2, \
    DATA_OFF_WORD_3
from utils.helpers import req_request


class SyncPremierScrapper:

    def __init__(self, **kwargs):
        self.main_parse_url = kwargs.get('main_parse_url')
        self.page_num = 1
        self.parsed_items = None
        self._is_day_end_flag = None

    @staticmethod
    def _get_usual_text(response) -> str:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        search_area = soup.find_all("div", {"class": "v-list"})
        if 'v-list premium-adv-list' in search_area[0]:
            return search_area[1]
        return search_area[0]

    @staticmethod
    def _form_urls(fresh_url_list: list) -> list:
        result = ['http://premier'+ x for x in fresh_url_list]
        return result

    @staticmethod
    def find_link(text: str) -> str:
        pattern = re.compile('href=\"(/.+\.html)\"><img')
        attached_link = re.findall(pattern, str(text))[0]
        print('attached_link: {}'.format(attached_link))
        return attached_link

    @staticmethod
    def _get_adv_main_body(text) -> str:
        pass

    @staticmethod
    def _prepare(adv_list) -> list:
        pass

    def filter_data_off(self, adv_list: list) -> list:
        adv_filtered_list = []
        for adv in adv_list:
            if DATA_OFF_WORD_1 in adv \
             or DATA_OFF_WORD_2 in adv or DATA_OFF_WORD_3 in adv:
                print('DAY OFF')
                self._is_day_end_flag = True
            else:
                adv_filtered_list.append(adv)
        return adv_filtered_list

    def _fetched_by_page_type(self, usual_text) -> list:
        adv_list_text = usual_text.split('<!-- c2 -->')
        adv_filtered_list = self.filter_data_off(adv_list_text)
        attached_links = [self.find_link(x) for x in adv_filtered_list]
        fetched_links = self._form_urls(attached_links)
        print(f'len fetched_link - {len(fetched_links)}')
        return fetched_links

    def _scrap(self, scrap_list) -> list:
        result = []
        for adv_link in scrap_list:
            response = req_request(method='GET',
                                   url=adv_link)
            main_text = self._get_adv_main_body(response.text)
            result_text = self._prepare(main_text)
            result.append(result_text)
        return result

    def main_scrap(self):
        try:
            while True:
                response = \
                    req_request("GET", url=self.main_parse_url +
                                PAGE_INDICATOR + str(self.page_num))

                usual_text = self._get_usual_text(response)
                fetched_adv_links = self._fetched_by_page_type(usual_text)

                self.parsed_items += (self._scrap(fetched_adv_links))

                if self._is_day_end_flag:
                    return self.parsed_items

                self.page_num += 1
                return self.parsed_items
        except Exception as ex:
            logging.error("Error while trying to parse: {}".format(str(ex)))


if __name__ == "__main__":
    import time
    link = 'https://premier.ua/zhilaia-nedvizhimost/prodazha-1-komn-kv-'
    link_2 = 'https://premier.ua/zhilaia-nedvizhimost/dachi'
    response = \
        requests.get(link)
    start = time.time()
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    search_area = soup.find_all("div", {"class": "v-list"})
    # print(search_area[1])
    import re
    pattern = re.compile('href=\"(/.+\.html)\"><img')
    attached_links = re.findall(pattern, str(search_area[1]))
    print(len(attached_links))
    for el in attached_links:
        print(el)

    # search2 = search_area.findChildren('v-list')
    # print(search2)




