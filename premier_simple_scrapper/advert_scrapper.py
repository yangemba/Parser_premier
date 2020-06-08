import lxml
from lxml.etree import Element
from lxml import etree
import logging
from lxml import html
import requests
import bs4

from utils.const import PAGE_INDICATOR
from utils.helpers import req_request


class SyncPremierScrapper:

    def __init__(self, **kwargs):
        self.main_parse_url = kwargs.get('main_parse_url')
        self.page_num = 1
        self.parsed_items = None

    @staticmethod
    def _get_usual_text(response) -> str:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        search_area = soup.find_all("div", {"class": "v-list"})
        if 'v-list premium-adv-list' in search_area[0]:
            return search_area[1]
        return search_area[0]

    def _is_day_end_flag(self) -> bool:
        if END_DAY_KEYWORDS in self.parsed_items[-1]:
            return True

    @staticmethod
    def _form_urls(fresh_url_list: list) -> list:
        result = ['http://premier'+ x for x in fresh_url_list]
        return result

    @staticmethod
    def _fetched_by_page_type(usual_text) -> list:
        pattern = re.compile('href=\"(/.+\.html)\"><img')
        attached_links = re.findall(pattern, str(usual_text))
        print(f'len fetched_link - {len(attached_links)}')
        return attached_links

    def _prepare(self, adv_list) -> list:
        pass

    @staticmethod
    def _get_adv_main_body(text) -> str:
        pass

    def _scrap(self, scrap_list) -> list:
        result = []
        for adv_link in scrap_list:
            response = req_request(method='GET',
                                   url=adv_link)
            main_text = self._get_adv_main_body(response.text)
            result.append(main_text)
        return result

    def main_scrap(self):
        try:
            while True:
                response = \
                    req_request("GET", url=self.main_parse_url +
                                PAGE_INDICATOR + str(self.page_num))

                usual_text = self._get_usual_text(response)
                fetched_adv_link = self._fetched_by_page_type(usual_text)

                self.parsed_items += \
                    (self._prepare(self._scrap(self._form_urls(fetched_adv_link))))
                if self._is_day_end_flag(self.usual_text):
                    break
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




