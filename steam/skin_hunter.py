from time import sleep
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from django.core.mail import EmailMultiAlternatives
from engine.setup_sel import SeleniumSetup


class SkinHunter(SeleniumSetup):
    urls_list = []
    gold_seeds = []
    blue_seeds = []

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

    def parse_url(self, urls):
        self.urls_list = []
        cond_list = ['Battle-Scarred', 'Well-Worn', 'Field-Tested', 'Minimal%20Wear', 'Factory%20New']
        urls = urls.split(sep=',')
        for url in urls:
            for condition in cond_list:
                self.urls_list.append(url.format(condition))
        return self.urls_list

    def wait_presence(self, xpath: str, click=False):
        reload = True
        while reload:
            sleep(5)
            try:
                if self.driver.find_element(By.XPATH, xpath):
                    reload = False
                    if click:
                        self.driver.find_element(By.XPATH, xpath).click()
            except NoSuchElementException:
                try:
                    if self.driver.find_element(By.XPATH, '//*[@id="searchResultsTable"]/div'):
                        reload = False
                except NoSuchElementException:
                    try:
                        if self.driver.find_element(By.XPATH,
                                                    '//*[contains(text(), "An error was encountered while processing your request:")]'):
                            sleep(240)
                            self.driver.refresh()
                    except NoSuchElementException:
                        self.driver.refresh()
                        continue

    def check_filter(self):
        if self.driver.find_element(By.XPATH, '//*[@id="ui-id-1-button"]/span[2]').text != '100':
            select = self.driver.find_element(By.XPATH, '//*[@id="ui-id-1"]')
            Select(select).select_by_value(100)

    def get_seeds_and_parse(self, gold_gem, blue_gem):
        elements = self.driver.find_elements(By.XPATH, '//*[@class="itemseed"]/span')
        for element in elements:
            if element.text != '':
                seed = int(element.text)
                if seed in gold_gem:
                    self.gold_seeds.append(int(seed))
                elif seed in blue_gem:
                    self.blue_seeds.append(int(seed))
        return self.gold_seeds, self.blue_seeds

    def shot_mail(self, data):

        html_content = render_to_string("steam/mail.html",
                                        {'data': data})

        body = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject='Steam Skin Seeker',
            body=body,
            from_email='jorge.mustafa@itmss.com.br',
            to=['jorginhomustafa@gmail.com'],
        )
        email.attach_alternative(html_content, 'text/html')
        if email.send():
            print('Email enviado')
