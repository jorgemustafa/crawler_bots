from django.core.management import BaseCommand
from twitch.watch_lives import MainMethods


class Command(BaseCommand):
    help = 'farm cs go skins in twitch.tv'

    def handle(self, *args, **options):
        tw = MainMethods()
        tw.login()
        tw.redirect()
        # tw.low_quality()
        tw.reload_video()
        # tw.chat()
