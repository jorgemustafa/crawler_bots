from django.core.management import BaseCommand
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twitch.selenium_script import MainMethods
from datetime import datetime
from time import sleep
from django.conf import settings
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from django.core.mail import send_mail


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        print(f'Inicio {datetime.now()}')
        driver_path = settings.CHROME_DRIVER_PATH
        steam_url = 'https://steamcommunity.com/market/listings/730/Five-SeveN%20%7C%20Case%20Hardened%20%28Field-Tested%29'
        options = ChromeOptions()
        # options.add_argument("--headless")  # disabling interface
        options.add_argument("--start-maximized")  # start chrome maximized
        options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
        options.add_argument("--mute-audio")  # mute audio
        options.add_extension('/home/musta/python/farm_bots/steam/steam-extension.crx')
        driver = Chrome(executable_path=driver_path, options=options)
        fe = driver.find_element
        actions = ActionChains(driver)

        # setting up sih
        driver.get('chrome-extension://cmeakgjggjdlcpncigglobpjbkabhmjl/dist/index.html#/settings/listingmarket')
        sleep(1)
        fe(By.XPATH, '//*[@id="resultnumber"]').send_keys(0)
        sleep(1)
        fe(By.XPATH, '//*[@id="root"]/div/main/div/div[1]/div/div[2]/div[2]/label/div/button').click()
        sleep(1)
        driver.get('chrome-extension://cmeakgjggjdlcpncigglobpjbkabhmjl/dist/index.html#/settings/general')
        sleep(1)
        Select(fe(By.XPATH, '//*[@id="cb_currency_code"]')).select_by_value('BRL')
        sleep(1)

        driver.get(steam_url)
        sleep(5)

        # while page not load, reload
        reload = True
        while reload:
            try:
                if fe(By.XPATH, '//*[@id="searchResultsRows"]'):
                    reload = False
                    break
            except NoSuchElementException:
                sleep(30)
                driver.refresh()
                continue

        # get skin data
        sleep(5)
        locator_h1 = By.XPATH, '//*[@id="largeiteminfo_item_name"]'
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located(locator_h1))
            fe(By.XPATH, '//*[contains(text(), "Get skin data, by default")]').click()
        except TimeoutException:
            driver.refresh()

        # wait until sih loads 100 items
        locator = By.XPATH, '//*[@id="listings"]/div[4]/div[2]/div[1]/div'
        try:
            WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element(locator, '1-100'))
        except TimeoutException:
            driver.refresh()

        # run all pages
        # pages = fe(By.XPATH, '//*[@id="searchResults_ctn"]/div[3]/div[2]/div').text
        # pages.split()
        # pages = int(pages[-1])
        # for page in pages:
        #     driver.get()

        # while page not load, reload
        reload = True
        while reload:
            try:
                if driver.find_elements(By.XPATH, '//*[@class="itemseed"]/span'):
                    reload = False
                    break
            except NoSuchElementException:
                driver.refresh()
                continue

        # get all seeds in page
        elements_seed = driver.find_elements(By.XPATH, '//*[@class="itemseed"]/span')
        seed_list = []
        for element in elements_seed:
            if element != '':
                seed = element.text
                seed_list.append(int(seed))

        # seeds that I want to follow
        gold_gem_list = [22, 107, 108, 156, 158, 164, 192, 195, 229, 257, 301, 308, 324, 338, 353, 356, 384, 393, 410,
                         427, 439, 440, 449, 451, 469, 473, 476, 486, 491, 504, 544, 546, 553, 565, 608, 621, 653, 660,
                         686, 691, 695, 703, 726, 731, 744, 747, 748, 759, 790, 805, 825, 860, 867, 895, 906, 929, 931,
                         946, 952, 959, 972, 976, 981]
        fade_gem_list = [381, 387, 399, 400, 420, 426, 428, 430, 436, 630, 661, 905, 955]
        blue_gem_list = [25, 151, 189, 278, 363, 532, 631, 648, 670, 690, 868, 872]

        set_seed_list = set(seed_list)
        set_gold_gem_list = set(gold_gem_list)
        set_fade_gem_list = set(fade_gem_list)
        set_blue_gem_list = set(blue_gem_list)
        if (set_seed_list & set_gold_gem_list
                or set_seed_list & set_fade_gem_list
                or set_seed_list & set_blue_gem_list):
            commons = set_seed_list & set_gold_gem_list \
                      or set_seed_list & set_fade_gem_list \
                      or set_seed_list & set_blue_gem_list
            print(commons)

            send_mail(
                subject='Steam Skin Seeker',
                message=f'Novas skins foram encontradas no mercado na url {steam_url}, confira a lista: Paint Seed:{commons}',
                from_email='bot@jorgemustafa.com.br',
                recipient_list=['jorginhomustafa@gmail.com'],
                fail_silently=False,
            )

        else:
            print('No common elements')


        # driver quit
        driver.quit()
