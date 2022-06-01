from datetime import datetime
from time import sleep
from django.conf import settings
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.common.by import By


class MainMethods:
    """
    This is a class to farm cs go skins in twitch
    """

    def __init__(self):
        self.user_tw = settings.USER_TWITCH
        self.pass_tw = settings.PASS_TWITCH
        self.twitch_url = 'https://www.twitch.tv'
        self.driver_path = settings.CHROME_DRIVER_PATH
        self.options = ChromeOptions()
        # self.options.add_argument("--headless")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--mute-audio")
        self.driver = Chrome(executable_path=self.driver_path, options=self.options)
        self.fe = self.driver.find_element
        self.actions = ActionChains(self.driver)

    def login(self):
        self.driver.get(self.twitch_url)
        self.fe(By.XPATH, '//*[@id="root"]/div/div[2]/nav/div/div[3]/div[3]/div/div[1]/div[1]/button/div/div').click()
        sleep(1)
        self.fe(By.XPATH, '/html/body/div[3]/div/div/div/div/div/div[1]/div/div')
        sleep(1)
        self.fe(By.XPATH, '//*[@id="login-username"]').send_keys(self.user_tw)
        sleep(1)
        self.fe(By.XPATH, '//*[@id="password-input"]').send_keys(self.pass_tw)
        sleep(1)
        self.fe(By.XPATH, '/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div[3]/form/div/div[3]/button').click()
        auth_code = input('Digite o codigo de autenticacao:')
        if auth_code == 'resend':
            self.fe(By.XPATH, '/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div[3]/div[3]/button').click()
            auth_code = input('Código reenviado, digite-o abaixo:')
        sleep(1)
        self.fe(By.XPATH,
                '/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div[3]/div[2]/div/div[1]/div/input').send_keys(
            auth_code)
        sleep(5)

    def redirect(self):
        self.driver.get('https://www.twitch.tv/csrfps')
        print('Assistindo...')

    def low_quality(self):
        video = self.fe(By.XPATH,
                        '//*[@id="root"]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div[3]')
        self.actions.move_to_element(video)
        self.fe(By.XPATH,
                '//*[@id="root"]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[3]/div/div[2]/div[2]/div[1]/div[2]/div/button').click()
        self.fe(By.XPATH,
                '//*[@id="root"]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[5]/div/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div/div/div[3]').click()
        self.fe(By.XPATH,
                '//*[@id="tw-83647b4914b76a83d09498cfda212654"]').click()

    def reload_video(self):
        x = 1
        while x < 2:
            try:
                self.driver.switch_to.default_content()
                self.fe(By.XPATH,
                        '//*[@id="root"]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[5]/div/div[3]/button')
                error = True
            except NoSuchElementException:
                error = False
            if error:
                sleep(60)
                self.driver.refresh()
                print(f'Página recarregada às {datetime.now()}')
                continue

    def chat(self):
        # chat = self.fe(By.XPATH,
        #                '//*[@id="481bcbbdca78742814014a36bda96fc8"]/div/div[1]/div/div/div/div/div/section/div/div[5]/div[2]/div[1]/div[2]/div/div/div[1]/div/textarea')
        # chat.send_keys('!trivelapoints')
        pass
