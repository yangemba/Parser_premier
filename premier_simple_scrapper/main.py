from premier_simple_scrapper.advert_scrapper import SyncPremierScrapper

if __name__ == "__main__":

    category_list = []

    for category in category_list:
        premier_scrapper = SyncPremierScrapper(main_parse_url=category)
        parsed_info = premier_scrapper.main_scrap()
        file_name = save_and_get_file(file_name)
        send_to_performing(file_name)









