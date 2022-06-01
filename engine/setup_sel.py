from datetime import datetime
from django.conf import settings
from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver import Keys


class SeleniumSetup:
    def __init__(self, ui=False, extensions=False):
        print(f'Início {datetime.now()}')
        self.options = ChromeOptions()
        if not ui:
            self.options.add_argument("--headless")
        if extensions:
            self.options.add_extension("/home/musta/python/crawler_bots/steam/steam-extension.crx")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--mute-audio")
        driver_path = settings.CHROME_DRIVER_PATH
        self.driver = Chrome(executable_path=driver_path, options=self.options)
        self.actions = ActionChains(self.driver)
        self.keys = Keys
