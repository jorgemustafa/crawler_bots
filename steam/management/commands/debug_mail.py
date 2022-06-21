from django.core.mail import EmailMultiAlternatives
from django.core.management import BaseCommand
from time import sleep
from datetime import datetime

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from steam.models import SkinData
from steam.skin_hunter import SkinHunter


class Command(BaseCommand):
    help = 'Hunter skins with rare patterns'

    def handle(self, *args, **options):
        data = 'teste'
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
