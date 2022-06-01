from django.core.management import BaseCommand
from time import sleep
from datetime import datetime
from steam.skin_hunter import SkinHunter, shot_mail
from steam.seeds.five_seven import GOLD_GEM, FADE_GEM, BLUE_GEM


class Command(BaseCommand):
    help = 'Hunter Five Seven'

    def handle(self, *args, **options):
        sh = SkinHunter(ui=True, extensions=True)
        sh.set_up_sih()
        sh.parse_url(weapon='five_seven', stattrak=True)
        data_email = {}
        for url in sh.urls_list:
            sleep(2)
            # sh.actions.send_keys(sh.keys.COMMAND+'t')
            sh.driver.get(url)
            sh.wait_presence(xpath='//*[@id="searchResultsRows"]')
            sh.wait_presence(xpath='//*[contains(text(), "Get skin data, by default" )]', click=True)
            sh.wait_presence(xpath='//*[@class="itemseed"]/span')
            # sh.check_filter()
            sh.get_seeds_and_parse(gold_gem=GOLD_GEM, fade_gem=FADE_GEM, blue_gem=BLUE_GEM)
            data_email = {url: {'gold': sh.gold_list, 'fade': sh.fade_list, 'blue': sh.blue_list}}
        shot_mail(data_email)
        print(f'Fim {datetime.now()}')