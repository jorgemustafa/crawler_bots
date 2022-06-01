from django.core.management import BaseCommand
from steam.skin_hunter import shot_mail


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        shot_mail('teste')
