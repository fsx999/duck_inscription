# coding=utf-8
from django.contrib.sites.models import Site
from mailrobot.models import Mail
from duck_inscription.models import Wish
from django.conf import settings
__author__ = 'paul'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        cod_etp = args[0]
        nb = args[1]
        mail = Mail.objects.get(name='email_inscription_ouverte')
        site = Site.objects.get(domain='preins.iedparis8.net')
        for wish in Wish.objects.filter(annee__cod_anu=2014,
                                        state='liste_attente_inscription',
                                        etape__cod_etp=str(cod_etp)).order_by('date_liste_inscription')[0:int(nb)]:
            email_etu = 'paul.guichon@iedparis8.net' if settings.DEBUG else wish.individu.email
            mail.make_message(
                recipients=(email_etu,),
                context={'wish': wish,
                         'site': site}
            ).send()
