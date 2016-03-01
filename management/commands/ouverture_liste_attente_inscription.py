# coding=utf-8
from django.contrib.sites.models import Site
from mailrobot.models import Mail
from duck_inscription.models import Wish
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('cod_etp', nargs='+')
        parser.add_argument('nb', nargs='+', type=int)

    def handle(self, *args, **options):
        cod_etp = options['cod_etp'][0]
        nb = options['nb'][0]
        mail = Mail.objects.get(name='email_inscription_ouverte')
        site = Site.objects.get(domain='preins.iedparis8.net')

        for wish in Wish.objects.filter(annee__cod_anu=2015,
                                        state='liste_attente_inscription',
                                        etape__cod_etp=str(cod_etp)).order_by('date_liste_inscription')[0:int(nb)]:
            email_etu = 'paul.guichon@iedparis8.net' if settings.DEBUG else wish.individu.personal_email
            wish.is_ok = True
            wish.dispatch()
            wish.save()
            mail.make_message(
                recipients=(email_etu,),
                context={'wish': wish,
                         'site': site}
            ).send()
