from django.core.management import BaseCommand
from datetime import datetime
from time import sleep
from django.conf import settings
from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.common.by import By


class Command(BaseCommand):
    help = 'farm money watching videos in hideout'

    def handle(self, *args, **options):
        print(f'Inicio {datetime.now()}')
        driver_path = settings.CHROME_DRIVER_PATH
        user = 'jorginhomustafa@gmail.com'
        password = 'Mohamet20@!'
        initial_url = 'https://hideout.co/login.php?'
        options = ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--mute-audio")
        driver = Chrome(executable_path=driver_path, options=options)
        fe = driver.find_element
        actions = ActionChains(driver)

        # login
        driver.get(initial_url)
        fe(By.XPATH, '//*[@id="username"]').send_keys(user)
        fe(By.XPATH, '//*[@id="password"]').send_keys(password)
        fe(By.XPATH, '//*[@id="login"]/div[4]/button').click()

        # choose short video
        sleep(10)
        durations = driver.find_elements(By.XPATH, '//*[@class="duration"]')
        list_durations = []
        for duration in durations:
            if duration.text != '':
                list_durations.append(duration.text)

        list_durations.sort()
        shorter_video = list_durations[0]
        driver.find_element(By.XPATH, f'//*[@class="duration"][contains(text(), "{shorter_video}")]').click()

        current_time = driver.find_element(By.XPATH, '//*[@class="brid-current-time-display"]').text
        duration_video = driver.find_element(By.XPATH, '//*[@class="brid-duration-display"]').text

        x = 1
        while x < 2:
            sleep(600)

        # parse if choose another video or continues watching by time

        # wait until video starts
        # WebDriverWait(driver, 20).until(
        #     EC.text_to_be_present_in_element((By.XPATH, '//*[@class="brid-current-time-display"]'), '00:01'))

        # wait until video ends
        # WebDriverWait(driver, 9999).until(
        #     EC.text_to_be_present_in_element((By.XPATH, '//*[@class="brid-current-time-display"]'), duration_video))
