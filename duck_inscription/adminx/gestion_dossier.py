# coding=utf-8
from __future__ import unicode_literals
import datetime
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, View
from openpyxl.writer.excel import save_virtual_workbook
from duck_inscription.xadmin_plugins.topnav import IEDPlugin
import test_duck_inscription.settings as preins_settings
from crispy_forms.bootstrap import TabHolder, Tab
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from mailrobot.models import Mail, MailBody, Address, Signature
from django.conf import settings
from xadmin.plugins.auth import UserAdmin
from xworkflows import InvalidTransitionError, ForbiddenTransition
from duck_inscription.forms.adminx_forms import DossierReceptionForm, EquivalenceForm, InscriptionForm, CandidatureForm
from xadmin.layout import Main, Fieldset, Container, Side, Row
from xadmin import views
import xadmin
from duck_inscription.models import Individu, SettingsEtape, WishWorkflow, SettingAnneeUni, WishParcourTransitionLog
from duck_inscription.models import Wish, SuiviDossierWorkflow, IndividuWorkflow, SettingsUser, CursusEtape
from xadmin.util import User
from xadmin.views import filter_hook, CommAdminView, BaseAdminView
from openpyxl import Workbook

class DossierReception(views.FormAdminView):
    form = DossierReceptionForm
    title = 'Dossier Reception'

    def get_redirect_url(self):
        return self.get_admin_url('dossier_receptionner')

    def post(self, request, *args, **kwargs):
        self.instance_forms()
        self.setup_forms()

        if self.valid_forms():
            code_dossier = self.form_obj.cleaned_data['code_dossier']

            try:
                wish = Wish.objects.get(code_dossier=code_dossier)
                if wish.state == 'equivalence':
                    wish.equivalence_receptionner()
                elif wish.state == 'candidature':
                    wish.candidature_reception()
                elif wish.state == 'inscription':
                    wish.inscription_reception()
                wish.envoi_email_reception()
                msg = u'''Le dossier {} avec l\'email {} est bien traité'''.format(wish.code_dossier,
                                                                                   wish.individu.personal_email)
                self.message_user(msg, 'success')
            except Wish.DoesNotExist:
                msg = u'Le dossier numéro {} n\'existe pas'.format(code_dossier)
                self.message_user(msg, 'error')
            except InvalidTransitionError:
                msg = u'Dossier déjà traité'
                self.message_user(msg, 'error')
            except ValueError:
                msg = u'Numéro dossier non valide'
                self.message_user(msg, 'error')
            return HttpResponseRedirect(self.get_redirect_url())
        return self.get_response()


class EquivalenceView(views.FormAdminView):
    title = 'Dossier équivalence'
    form = EquivalenceForm

    def get_form_datas(self, **kwargs):
        data = super(EquivalenceView, self).get_form_datas(**kwargs)
        queryset = getattr(self.request.user.setting_user, 'etapes', SettingsEtape.objects).all()

        data.update({'queryset': queryset})
        return data

    def post(self, request, *args, **kwargs):
        self.instance_forms()
        self.setup_forms()

        if self.valid_forms():
            code_dossier = self.form_obj.cleaned_data['code_dossier']
            choix = self.form_obj.cleaned_data['choix']
            etape = self.form_obj.cleaned_data['etapes']
            self.motif = self.form_obj.cleaned_data['motif']

            try:
                wish = Wish.objects.get(code_dossier=code_dossier)
                if wish.etape not in self.request.user.setting_user.etapes.all():
                    raise PermissionDenied
                if wish.suivi_dossier.is_equivalence_traite:
                    msg = 'Dossier déjà traité'
                    self.message_user(msg, 'warning')
                elif not wish.state.is_equivalence:
                    msg = 'Dossier n\'est pas en equivalence'
                    self.message_user(msg, 'warning')
                elif choix == 'complet':
                    try:
                        wish.equivalence_complet()
                        template = Mail.objects.get(name='email_equivalence_complet')
                        self._envoi_email(wish, template)
                        self.message_user('Dossier traité', 'success')
                    except InvalidTransitionError as e:
                        if wish.suivi_dossier.is_equivalence_complet:
                            msg = 'Dossier déjà traité'
                            self.message_user(msg, 'warning')
                        elif wish.suivi_dossier.is_inactif:
                            wish.equivalence_receptionner()
                            wish.equivalence_complet()
                            self.message_user('Dossier traité', 'success')
                        else:
                            raise e

                elif choix == 'incomplet':
                    try:

                        wish.equivalence_incomplet()
                    except InvalidTransitionError as e:
                        if wish.suivi_dossier.is_inactif:
                            wish.equivalence_receptionner()
                            wish.equivalence_incomplet()

                        else:
                            raise e
                    self.message_user('Dossier traité', 'success')
                    self._envoi_email(wish, Mail.objects.get(name='email_equivalence_incomplet'))

                elif choix == 'accepte':
                    mail = 'email_equivalence_accepte' if wish.etape == etape else 'email_equivalence_reoriente'

                    try:
                        wish.equivalence_traite()
                    except (InvalidTransitionError, ForbiddenTransition) as e:
                        if wish.suivi_dossier.is_inactif:
                            wish.equivalence_receptionner()
                            wish.equivalence_complet()
                            wish.equivalence_traite()
                        elif wish.suivi_dossier.is_equivalence_reception:
                            wish.equivalence_complet()
                            wish.equivalence_traite()
                        elif wish.suivi_dossier.is_equivalence_incomplet:
                            wish.equivalence_complet()
                            wish.equivalence_traite()
                        else:
                            raise e
                    wish.etape = etape
                    wish.save()
                    wish.ouverture_candidature()

                    self._envoi_email(wish, Mail.objects.get(name=mail))
                    self.message_user('Dossier traité', 'success')
                elif choix == 'refuse':
                    try:
                        wish.equivalece_refuse()
                        self._envoi_email(wish, Mail.objects.get(name='email_equivalence_refuse'))
                        self.message_user('Dossier traité', 'success')
                    except InvalidTransitionError as e:
                        raise e

                # on clean le form
                self.form_obj.data = self.form_obj.data.copy()
                self.form_obj.data['code_dossier'] = None

            except Wish.DoesNotExist:
                msg = 'Le dossier n\'existe pas'
                self.message_user(msg, 'error')
            except PermissionDenied:
                msg = 'Vous n\'avez pas la permission de traité ce dossier'
                self.message_user(msg, 'error')
            except InvalidTransitionError as e:
                self.message_user(e, 'error')

        return self.get_response()

    def get_redirect_url(self):
        return self.get_admin_url('dossier_equivalence')

    def _envoi_email(self, wish, template):
        context = {'site': Site.objects.get(id=preins_settings.SITE_ID), 'wish': wish, 'motif': self.motif}
        email = wish.individu.user.email if not settings.DEBUG else 'paul.guichon@iedparis8.net'
        mail = template.make_message(context=context, recipients=[email])
        mail.send()


class CandidatureView(views.FormAdminView):
    title = 'Dossier candidature'
    form = CandidatureForm

    def post(self, request, *args, **kwargs):
        self.instance_forms()
        self.setup_forms()

        if self.valid_forms():
            code_dossier = self.form_obj.cleaned_data['code_dossier']
            choix = self.form_obj.cleaned_data['choix']
            self.motif = self.form_obj.cleaned_data['motif']

            try:
                wish = Wish.objects.get(code_dossier=code_dossier)
                if wish.etape not in self.request.user.setting_user.etapes.all():
                    raise PermissionDenied
                if wish.suivi_dossier.is_candidature_traite or wish.suivi_dossier.is_candidature_refuse:
                    msg = 'Dossier déjà traité'
                    self.message_user(msg, 'warning')
                elif not wish.state.is_candidature and not wish.state.is_liste_attente_candidature:
                    msg = 'Dossier n\'est pas en candidature'
                    self.message_user(msg, 'warning')
                elif choix == 'complet':
                    template = Mail.objects.get(name='email_candidature_complet')
                    try:
                        wish.candidature_complet()
                    except InvalidTransitionError as e:
                        if wish.suivi_dossier.is_candidature_complet:
                            msg = 'Dossier déjà traité'
                            self.message_user(msg, 'warning')
                        elif wish.suivi_dossier.is_inactif:
                            wish.candidature_reception()
                            wish.candidature_complet()
                            self.message_user('Dossier traité', 'success')
                        else:
                            raise e
                    self._envoi_email(wish, template)
                    self.message_user('Dossier traité', 'success')

                elif choix == 'incomplet':
                    try:
                        wish.candidature_incomplet()
                    except InvalidTransitionError as e:
                        if wish.suivi_dossier.is_inactif:
                            wish.candidature_reception()
                            wish.candidature_incomplet()
                        else:
                            raise e
                    self.message_user('Dossier traité', 'success')
                    self._envoi_email(wish, Mail.objects.get(name='email_candidature_incomplet'))

                elif choix == 'accepte':
                    mail = 'email_candidature_accepte'

                    try:
                        wish.candidature_traite()
                    except (InvalidTransitionError, ForbiddenTransition) as e:
                        if wish.suivi_dossier.is_inactif:
                            wish.candidature_reception()
                            wish.candidature_complet()
                            wish.candidature_traite()
                        elif wish.suivi_dossier.is_candidature_reception:
                            wish.candidature_complet()
                            wish.candidature_traite()
                        elif wish.suivi_dossier.is_candidature_incomplet:
                            wish.candidature_complet()
                            wish.candidature_traite()
                    wish.is_ok = True
                    wish.save()
                    wish.ouverture_inscription()

                    self._envoi_email(wish, Mail.objects.get(name=mail))
                    self.message_user('Dossier traité', 'success')
                elif choix == 'refuse':
                    try:
                        wish.candidature_refuse()
                        self._envoi_email(wish, Mail.objects.get(name='email_candidature_refuse'))
                        self.message_user('Dossier traité', 'success')
                    except InvalidTransitionError as e:
                        raise e
                elif choix == 'attente':
                    self._envoi_email(wish, Mail.objects.get(name='email_candidature_attente'))
                    self.message_user('Dossier traité', 'success')
                elif choix == 'ouvert':
                    wish.candidature()
                    self._envoi_email(wish, Mail.objects.get(name='email_candidature_ouverte'))
                    self.message_user('Dossier traité', 'success')
                # on clean le form
                self.form_obj.data = self.form_obj.data.copy()
                self.form_obj.data['code_dossier'] = None

            except Wish.DoesNotExist:
                msg = 'Le dossier n\'existe pas'
                self.message_user(msg, 'error')
            except PermissionDenied:
                msg = 'Vous n\'avez pas la permission de traité ce dossier'
                self.message_user(msg, 'error')
            except InvalidTransitionError as e:
                self.message_user(e, 'error')

        return self.get_response()

    def get_redirect_url(self):
        return self.get_admin_url('dossier_candidature')

    def _envoi_email(self, wish, template):
        context = {'site': Site.objects.get(id=preins_settings.SITE_ID), 'wish': wish, 'motif': self.motif}
        email = wish.individu.user.email if not settings.DEBUG else 'paul.guichon@iedparis8.net'
        mail = template.make_message(context=context, recipients=[email])
        mail.send()


class DossierInscriptionView(views.FormAdminView):
    form = InscriptionForm
    title = 'Dossier Inscription'

    def get_redirect_url(self):
        return self.get_admin_url('traitement_inscription')

    def post(self, request, *args, **kwargs):
        self.instance_forms()
        self.setup_forms()

        if self.valid_forms():
            code_dossier = self.form_obj.cleaned_data['code_dossier']
            choix = self.form_obj.cleaned_data['choix']

            self.motif = self.form_obj.cleaned_data['motif']

            try:
                wish = Wish.objects.get(code_dossier=code_dossier)
                if wish.etape not in self.request.user.setting_user.etapes.all():
                    raise PermissionDenied
                if wish.suivi_dossier.is_inscription_traite or wish.suivi_dossier.is_inscription_refuse:
                    msg = 'Dossier déjà traité'
                    self.message_user(msg, 'warning')
                elif not wish.state.is_inscription and not wish.state.is_liste_attente_inscription:
                    msg = 'Dossier n\'est pas en inscription'
                    self.message_user(msg, 'warning')
                elif choix == 'complet':
                    template = Mail.objects.get(name='email_inscription_complet')
                    try:
                        wish.inscription_complet()
                        self._envoi_email(wish, template)
                        self.message_user('Dossier traité', 'success')
                    except InvalidTransitionError as e:
                        if wish.suivi_dossier.is_inscription_complet:
                            msg = 'Dossier déjà traité'

                            self.message_user(msg, 'warning')
                        elif wish.suivi_dossier.is_inactif:
                            wish.inscription_reception()
                            wish.inscription_complet()
                            self._envoi_email(wish, template)
                            self.message_user('Dossier traité', 'success')
                        else:
                            raise e

                elif choix == 'incomplet':
                    try:

                        wish.inscription_incomplet()
                    except InvalidTransitionError as e:
                        if wish.suivi_dossier.is_inactif:
                            wish.inscription_reception()
                            wish.inscription_incomplet()

                        else:
                            raise e
                    self.message_user('Dossier traité', 'success')
                    self._envoi_email(wish, Mail.objects.get(name='email_inscription_incomplet'))
                elif choix == 'incomplet_renvoi':
                    try:

                        wish.inscription_incomplet_renvoi()
                    except InvalidTransitionError as e:
                        if wish.suivi_dossier.is_inactif:
                            wish.inscription_reception()
                            wish.inscription_incomplet_renvoi()
                        else:
                            raise e
                    self.message_user('Dossier traité', 'success')
                    self._envoi_email(wish, Mail.objects.get(name='email_inscription_incomplet_renvoi'))
                elif choix == 'ouvert':
                    try:
                        wish.is_ok = True
                        wish.inscription()
                        wish.save()
                    except (InvalidTransitionError, ForbiddenTransition) as e:
                        raise e
                    self._envoi_email(wish, Mail.objects.get(name='email_inscription_ouverte'))
                    self.message_user('Dossier traité', 'success')
                elif choix == 'refuse':
                    try:
                        wish.inscription_refuse()
                        self._envoi_email(wish, Mail.objects.get(name='email_inscription_refuse'))
                        self.message_user('Dossier traité', 'success')
                    except InvalidTransitionError as e:
                        raise e

                # on clean le form
                self.form_obj.data = self.form_obj.data.copy()
                self.form_obj.data['code_dossier'] = None

            except Wish.DoesNotExist:
                msg = 'Le dossier n\'existe pas'
                self.message_user(msg, 'error')
            except PermissionDenied:
                msg = 'Vous n\'avez pas la permission de traité ce dossier'
                self.message_user(msg, 'error')
            except InvalidTransitionError as e:
                self.message_user(e, 'error')

        return self.get_response()

    def _envoi_email(self, wish, template):
        context = {'site': Site.objects.get(id=preins_settings.SITE_ID), 'wish': wish, 'motif': self.motif}
        email = wish.individu.user.email if not settings.DEBUG else 'paul.guichon@iedparis8.net'
        mail = template.make_message(context=context, recipients=[email])
        mail.send()


xadmin.site.register_view(r'^dossier_receptionner/$', DossierReception, 'dossier_receptionner')
xadmin.site.register_view(r'^dossier_equivalence/$', EquivalenceView, 'dossier_equivalence')
xadmin.site.register_view(r'^dossier_candidature/$', CandidatureView, 'dossier_candidature')
xadmin.site.register_view(r'^traitement_inscription/$', DossierInscriptionView, 'traitement_inscription')
