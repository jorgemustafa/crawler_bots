from django.core.management import BaseCommand
from time import sleep
from datetime import datetime
from steam.models import SkinData
from steam.skin_hunter import SkinHunter


class Command(BaseCommand):
    help = 'Hunter skins with rare patterns'

    def handle(self, *args, **options):
        data_mail_list = []
        SH = SkinHunter(ui=True, extensions=True)
        SH.set_up_sih()
        for skin in SkinData.objects.all():
            SH.parse_url(urls=skin.urls)
            gold = skin.gold.split(sep=',')
            gold = list(map(int, gold))
            blue = skin.blue.split(sep=',')
            blue = list(map(int, blue))
            for url in SH.urls_list:
                sleep(2)
                SH.driver.get(url)
                SH.wait_presence(xpath='//*[@id="searchResultsRows"]')
                SH.wait_presence(xpath='//*[contains(text(), "Get skin data, by default" )]', click=True)
                SH.wait_presence(xpath='//*[@class="itemseed"]/span')
                SH.get_seeds_and_parse(gold_gem=gold, blue_gem=blue)
                data_loop = {'skin': skin.weapon, 'url': url, 'gold': SH.gold_seeds, 'blue': SH.blue_seeds}
                if len(data_loop['gold']) != 0 or len(data_loop['blue']) != 0:
                    data_mail_list.append(data_loop)
                    SH.gold_seeds = []
                    SH.blue_seeds = []
        if len(data_mail_list) != 0:
            SH.shot_mail(data=data_mail_list)
        print(f'Fim {datetime.now()}')
