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
        for skin in SkinData.objects.filter(active=True):
            SH.parse_url(urls=skin.urls)
            if skin.gold == '':
                skin.gold = '0'
            gold_list = skin.gold.split(sep=',')
            gold_list = list(map(int, gold_list))
            if skin.blue == '':
                skin.blue = '0'
            blue_list = skin.blue.split(sep=',')
            blue_list = list(map(int, blue_list))
            for url in SH.urls_list:
                sleep(2)
                SH.driver.get(url)
                SH.wait_presence(xpath='//*[@id="searchResultsRows"]')
                SH.wait_presence(xpath='//*[contains(text(), "Get skin data, by default" )]', click=True)
                SH.wait_presence(xpath='//*[@class="itemseed"]/span')
                SH.get_seeds_and_parse(gold_gem=gold_list, blue_gem=blue_list)
                if len(SH.gold_seeds) != 0 or len(SH.blue_seeds) != 0:
                    data_loop = {'skin': skin.weapon, 'url': url, 'gold': SH.gold_seeds, 'blue': SH.blue_seeds}
                    data_mail_list.append(data_loop)
                SH.gold_seeds = []
                SH.blue_seeds = []
        if len(data_mail_list) != 0:
            SH.shot_mail(data=data_mail_list)
        else:
            print('nenhum dado')
        print(f'Fim {datetime.now()}')
        return
