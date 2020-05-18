import bs4
import logging

from utils.const import PAGE_INDICATOR
from utils.helpers import req_request


class SyncPremierScrapper:

    def __init__(self, **kwargs):
        self.main_parse_url = kwargs.get('main_parse_url')
        self.page_num = 1
        self.parsed_items = None

    def _categorise_response(self) -> str:
        pass

    def _fetched_by_page_type(self) -> list:
        pass

    def _prepare(self) -> list:
        pass

    @staticmethod
    def _cut_adv_main_body(text) -> str:
        pass

    def _scrap(self, scrap_list) -> list:
        result = []
        for adv_link in scrap_list:
            response = req_request(method='GET',
                                   url=adv_link)
            main_text = self._cut_adv_main_body(response.text)
            result.append(main_text)
        return result

    def main_scrap(self):
        try:
            while True:
                response = \
                    req_request(url=self.main_parse_url +
                                PAGE_INDICATOR + str(self.page_num))
                category = self._categorise_response(response.text)
                fetched_adv_link = self._fetched_by_page_type(category)
                self.parsed_items += \
                    (self._prepare(self._scrap(fetched_adv_link)))
                if len(fetched_adv_link) < 10:
                    break
                self.page_num += 1
            return self.parsed_items
        except Exception as ex:
            logging.error("Error while trying to parse: {}".format(str(ex)))






