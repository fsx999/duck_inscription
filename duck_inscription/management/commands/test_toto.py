# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.db import IntegrityError
from django_xworkflows.xworkflow_log.models import TransitionLog
from mailrobot.models import Mail
from django_apogee.models import AnneeUni, VersionEtape as VersionEtapeApogee, EtpGererCge, Etape
from duck_inscription.models import SettingAnneeUni, SettingsEtape, Wish, WishTransitionLog, WishParcourTransitionLog



class Command(BaseCommand):
    def handle(self, *args, **options):
        # on récupére les personnes du jour (soit la date de création, de modif plus grand que la veille
        # mail = Mail.objects.get(name='email_inscription_ouverte')
        # site = Site.objects.get(domain='preins.iedparis8.net')
        # print WishTransitionLog.objects.filter(wish__etape__cod_etp='L3NEDU',
                                               # to_state='inscription_reception').count()
        text = u"""
ELECTION DES REPRESENTANTS DES ETUDIANTS
AU CONSEIL DE L’IED

mardi 9 décembre 2014
salle D  201 (bâtiment D, 2ème étage)



Comme toutes les composantes de l’Université, l’IED est administré par un Conseil dont la composition est fixée par ses statuts : deux professeurs, deux maîtres de conférences, deux chargés d’enseignements, deux représentants du personnel administratif et deux étudiants auxquels s’ajoutent dix personnalités extérieures.

Actuellement, les deux sièges des représentants des étudiants (des usagers) sont à renouveler. Pour les pourvoir, le scrutin est prévu le mardi 9 décembre 2014. Le bureau de vote sera ouvert de 9h30 à 17h30 en salle D201.

Le scrutin est un scrutin de liste à la proportionnelle avec répartition des sièges à restant à pourvoir selon la règle du plus fort reste. Les listes de candidature doivent comporter pour chaque candidat titulaire le nom d’un suppléant. Une liste peut être incomplète. Dans ce cas elle peut ne comporter qu’un seul candidat (et son suppléant).

Tous les électeurs sont éligibles. Tous les étudiants régulièrement inscrits à l’IED au titre de l’année universitaire 2014-2015 sont électeurs. La durée du mandat est de deux ans à condition que l’élu garde sa qualité d’étudiant à l’IED.

Les candidats souhaitant former une liste devront remplir le formulaire de déclaration de liste ainsi que le formulaire de candidature individuelle  (chaque candidat figurant sur la liste devra impérativement  effectuer une déclaration individuelle). Ces formulaires seront téléchargeables très prochainement sur la plate forme IED dans le dossier « Espace commun aux formations IED », rubrique « élection des représentants usagers au Conseil de l'IED ». Les candidats devront y joindre une photocopie de leur carte d’étudiant ou à défaut le certificat de scolarité de l’année en cours accompagné de la photocopie d’une pièce d’identité.
Les membres d’une liste peuvent rédiger une « profession de foi » (2 pages maximum) qui sera jointe à la liste et aux déclarations individuelles de candidatures.

Les listes devront être composées alternativement d’un candidat de chaque sexe. Les candidats apparaissent sur la liste par ordre préférentiel.

Une rubrique « Election » sera ouverte sur la plateforme de l’IED dans l’espace commun aux formations où seront disponibles les statuts de l’IED, les différents documents à télécharger et toutes les informations utiles au bon déroulement de ce scrutin. Un forum sera également ouvert afin de faciliter les échanges entre les étudiants.
        """

        for x in Wish.objects.filter(etape_dossier__to_state='inscription_reception'):
            send_mail('[IED] Election', text, 'nepasrepondre@iedparis8.net', [x.individu.personal_email])



