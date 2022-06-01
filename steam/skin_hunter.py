from time import sleep
import pandas as pd
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from django.core.mail import EmailMultiAlternatives
from engine.setup_sel import SeleniumSetup
from .weapons_urls import *


class SkinHunter(SeleniumSetup):
    urls_list = []
    seeds = None

    def __init__(self, ui, extensions):
        SeleniumSetup.__init__(self, ui, extensions)

    def set_up_sih(self):
        self.driver.get('chrome-extension://cmeakgjggjdlcpncigglobpjbkabhmjl/dist/index.html#/settings/listingmarket')
        sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="resultnumber"]').send_keys(0)
        sleep(1)
        self.driver.find_element(By.XPATH,
                                 '//*[@id="root"]/div/main/div/div[1]/div/div[2]/div[2]/label/div/button').click()
        sleep(1)
        self.driver.get('chrome-extension://cmeakgjggjdlcpncigglobpjbkabhmjl/dist/index.html#/settings/general')
        sleep(1)
        Select(self.driver.find_element(By.XPATH, '//*[@id="cb_currency_code"]')).select_by_value('BRL')
        sleep(1)

    def parse_url(self, weapon: str, stattrak=False):
        cond_list = ['Battle-Scarred', 'Well-Worn', 'Field-Tested', 'Minimal%20Wear', 'Factory%20New']
        if weapon == 'five_seven':
            for condition in cond_list:
                self.urls_list.append(FIVE_SEVEN_URL.format(condition))
        if stattrak:
            for condition in cond_list:
                self.urls_list.append((FIVE_SEVEN_STT_URL.format(condition)))
        return self.urls_list

    def wait_presence(self, xpath: str, click=False):
        reload = True
        while reload:
            try:
                sleep(10)  # todo alterar para 20
                if self.driver.find_element(By.XPATH, xpath):
                    reload = False
                    if click:
                        self.driver.find_element(By.XPATH, xpath).click()
            except NoSuchElementException:
                self.driver.refresh()
                continue

    def check_filter(self):
        if self.driver.find_element(By.XPATH, '//*[@id="ui-id-1-button"]/span[2]').text != '100':
            select = self.driver.find_element(By.XPATH, '//*[@id="ui-id-1"]')
            Select(select).select_by_value(100)

    def get_seeds_and_parse(self, gold_gem, fade_gem, blue_gem):
        elements_seed = self.driver.find_elements(By.XPATH, '//*[@class="itemseed"]/span')
        all_seeds = []
        seeds = {}
        for element in elements_seed:
            seed = element.text
            if seed != '':
                all_seeds.append(int(seed))

        set_seed = set(all_seeds)
        set_gold_gem = set(gold_gem)
        set_fade_gem = set(fade_gem)
        set_blue_gem = set(blue_gem)
        if (set_seed & set_gold_gem
                or set_seed & set_fade_gem
                or set_seed & set_blue_gem):
            seeds = set_seed & set_gold_gem \
                    or set_seed & set_fade_gem \
                    or set_seed & set_blue_gem

        return self.separate_by_tier(seeds, gold_gem, fade_gem, blue_gem)

    def separate_by_tier(self, seeds, gold, fade, blue):
        # separate seed by tier
        self.gold_list = []
        self.fade_list = []
        self.blue_list = []
        for seed in seeds:
            if seed in gold:
                self.gold_list.append(seed)
            elif seed in fade:
                self.fade_list.append(seed)
            elif seed in blue:
                self.blue_list.append(seed)

        return self.gold_list, self.fade_list, self.blue_list

    def shot_mail(self, data):

        msg_list = []
        for item in data:
            url = item['url']
            gold = item['gold']
            fade = item['fade']
            blue = item['blue']
            msg_list.append(f'{url} | Gold GEM: {gold}, Blue GEM: {blue}, Fade GEM: {fade}')

        html_content = render_to_string("steam/mail.html", {'msg': msg_list})
        body = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject='Steam Skin Seeker',
            body=body,
            from_email='bot@jorgemustafa.com.br',
            to=['jorginhomustafa@gmail.com'],
        )
        email.attach_alternative(html_content, 'text/html')
        if email.send():
            print('Email enviado')

    # run all pages
    # pages = self.driver.find_element(By.XPATH, '//*[@id="searchResults_ctn"]/div[3]/div[2]/div').text
    # pages.split()
    # pages = int(pages[-1])
    # for page in pages:
    #     self.driver.get()
