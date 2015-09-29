# coding=utf-8
from __future__ import unicode_literals
from duck_inscription.models import Wish
from django.core.management.base import BaseCommand
from django.core.mail import send_mail


class Command(BaseCommand):
    def handle(self, *args, **options):
        text = """
Bonjour,

Suite à un problème technique sur notre site, une étape importante de la procédure de candidature n'a pas été effectuée. Afin de régulariser la situation merci de vous connecter à nouveau à votre compte (Candidature) et de renseigner :

Vos résultats pour la candidature du Master 2

Moyenne générale
Note de stage
Note du Mémoire du Master 1


et pour la candidature de Master 1

Moyenne générale seulement

Il n'y a rien d'autre à faire.

Cordialement
        """

        for wish in Wish.objects.filter(etape__cod_etp__in=['M1NPCL', 'M2NPCL'], state='candidature'):
            send_mail('[IED] Problème de candidature important', text, 'nepasrepondre@iedparis8.net', [wish.individu.personal_email])
            wish.state = 'note_master'
            wish.save()
        print "fini"