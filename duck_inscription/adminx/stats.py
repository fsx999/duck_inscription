# coding=utf-8
from __future__ import unicode_literals
from datetime import date
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from openpyxl.workbook import Workbook
from openpyxl.writer.excel import save_virtual_workbook
import xlwt
from django_apogee.models import InsAdmEtp
from xadmin.views import filter_hook, BaseAdminView
from xadmin import views
import xadmin
import datetime
from duck_inscription.models import SettingsEtape, NoteMasterModel
from duck_inscription.models import Wish


class StatistiquePal(views.Dashboard):
    base_template = 'statistique/stats_pal.html'
    widget_customiz = False

    def get_context(self):
        context = super(StatistiquePal, self).get_context()
        context['etapes'] = SettingsEtape.objects.filter(is_inscription_ouverte=True).order_by('diplome')
        return context

    @filter_hook
    def get_breadcrumb(self):
        return [{'url': self.get_admin_url('index'), 'title': 'Accueil'},
                {'url': self.get_admin_url('statistiques'), 'title': 'Statistique'},
                {'url': self.get_admin_url('stats_pal'), 'title': 'Statistique PAL'}]

    @never_cache
    def get(self, request, *args, **kwargs):
        self.widgets = self.get_widgets()
        return self.template_response(self.base_template, self.get_context())
xadmin.site.register_view(r'^stats_pal/$', StatistiquePal, 'stats_pal')


class StatistiquePiel(views.Dashboard):
    base_template = 'statistique/stats_piel.html'
    widget_customiz = False

    @filter_hook
    def get_context(self):
        context = super(StatistiquePiel, self).get_context()
        context['etapes'] = SettingsEtape.objects.filter(is_inscription_ouverte=True).order_by('diplome')
        return context

    @never_cache
    def get(self, request, *args, **kwargs):
        self.widgets = self.get_widgets()
        return self.template_response(self.base_template, self.get_context())

    @filter_hook
    def get_breadcrumb(self):
        return [{'url': self.get_admin_url('index'), 'title': 'Accueil'},
                {'url': self.get_admin_url('statistiques'), 'title': 'Statistique'},
                {'url': self.get_admin_url('stats_piel'), 'title': 'Statistique PIEL'}]
xadmin.site.register_view(r'^stats_piel/$', StatistiquePiel, 'stats_piel')


class StatistiqueApogee(views.Dashboard):
    base_template = 'statistique/stats_apogee.html'
    widget_customiz = False

    @filter_hook
    def get_context(self):
        context = super(StatistiqueApogee, self).get_context()
        context['etapes'] = SettingsEtape.objects.filter(is_inscription_ouverte=True).order_by('diplome')
        return context

    @never_cache
    def get(self, request, *args, **kwargs):
        self.widgets = self.get_widgets()
        return self.template_response(self.base_template, self.get_context())

    @filter_hook
    def get_breadcrumb(self):
        return [{'url': self.get_admin_url('index'), 'title': 'Accueil'},
                {'url': self.get_admin_url('statistiques'), 'title': 'Statistique'},
                {'url': self.get_admin_url('stats_apogee'), 'title': 'Statistique Apogee'}]
xadmin.site.register_view(r'^stats_apogee/$', StatistiqueApogee, 'stats_apogee')


class ExtrationStatistique(BaseAdminView):
    def get(self, request, *args, **kwargs):
        type_stat = kwargs.get('type_stat', 'stat_parcours_dossier')

        wb = Workbook()
        ws = wb.active

        if type_stat == 'parcours_dossier':
            queryset = Wish.objects.filter(etape__cod_etp=kwargs['step'], parcours_dossier__to_state=kwargs['etat'])
        elif type_stat == 'state':
            queryset = Wish.objects.filter(state=kwargs['etat'], etape__cod_etp=kwargs['step'])
        else:
            queryset = Wish.objects.filter(etape_dossier__to_state=kwargs['etat'], etape__cod_etp=kwargs['step'])
        ws.cell(row=1, column=1).value = 'Numero Etudiant:'
        ws.cell(row=1, column=2).value = 'Nom patronimique:'
        ws.cell(row=1, column=3).value = "Nom d'époux:"
        ws.cell(row=1, column=4).value = "Prénom:"
        ws.cell(row=1, column=5).value = "Deuxiéme prénom"
        ws.cell(row=1, column=6).value = "Email:"
        for row, wish in enumerate(queryset):
            ws.cell(row=row + 2, column=1).value = wish.individu.student_code
            ws.cell(row=row + 2, column=2).value = wish.individu.last_name
            ws.cell(row=row + 2, column=3).value = wish.individu.common_name
            ws.cell(row=row + 2, column=4).value = wish.individu.first_name1
            ws.cell(row=row + 2, column=5).value = wish.individu.first_name2
            ws.cell(row=row + 2, column=6).value = wish.individu.personal_email


        response = HttpResponse(save_virtual_workbook(wb), mimetype='application/vnd.ms-excel')
        date = datetime.datetime.today().strftime('%d-%m-%Y')
        response['Content-Disposition'] = 'attachment; filename=%s_%s.xlsx' % ('extraction', date)
        return response
xadmin.site.register_view(r'^extraction/(?P<type_stat>\w+)/(?P<etat>\w+)/(?P<step>\w+)/$', ExtrationStatistique,
                          'extraction_stat')


class ExtractionStatApogee(BaseAdminView):
    def get(self, request, *args, **kwargs):
        cod_etp, annee = kwargs['step'], kwargs['annee']
        queryset = InsAdmEtp.inscrits.filter(cod_anu=annee, cod_etp=cod_etp)
        wb = Workbook()
        ws = wb.active
        ws.cell(row=1, column=1).value = 'Numero Etudiant:'
        ws.cell(row=1, column=2).value = 'Nom patronimique:'
        ws.cell(row=1, column=3).value = "Nom d'époux:"
        ws.cell(row=1, column=4).value = "Prénom:"
        ws.cell(row=1, column=5).value = "Deuxiéme prénom"
        ws.cell(row=1, column=6).value = "Email Perso:"
        ws.cell(row=1, column=7).value = "Email Foad"
        ws.cell(row=1, column=8).value = "Reinscription:"
        for row, etp in enumerate(queryset):
            ind = etp.cod_ind
            ws.cell(row=row + 2, column=1).value = ind.cod_etu
            ws.cell(row=row + 2, column=2).value = ind.lib_nom_pat_ind
            ws.cell(row=row + 2, column=3).value = ind.lib_nom_usu_ind
            ws.cell(row=row + 2, column=4).value = ind.lib_pr1_ind
            ws.cell(row=row + 2, column=5).value = ind.lib_pr2_ind
            ws.cell(row=row + 2, column=6).value = str(ind.get_email(annee))
            ws.cell(row=row + 2, column=7).value = str(ind.cod_etu) + '@foad.iedparis8.net'
            ws.cell(row=row + 2, column=8).value = "Oui" if etp.is_reins else "Non"



        response = HttpResponse(save_virtual_workbook(wb), mimetype='application/vnd.ms-excel')
        date = datetime.datetime.today().strftime('%d-%m-%Y')
        response['Content-Disposition'] = 'attachment; filename=%s_%s_%s.xlsx' % ('extraction_apogee', cod_etp, date)
        return response

xadmin.site.register_view(r'^extraction_apogee/(?P<annee>\w+)/(?P<step>\w+)/$', ExtractionStatApogee,
                          'extraction_apogee')


class ExtractionPiel(views.Dashboard):
    base_template = 'extraction/extraction_pal.html'
    widget_customiz = False

    @filter_hook
    def get_context(self):
        context = super(ExtractionPiel, self).get_context()
        context['etapes'] = SettingsEtape.objects.filter(is_inscription_ouverte=True).order_by('diplome')
        return context

    @never_cache
    def get(self, request, *args, **kwargs):
        self.widgets = self.get_widgets()
        return self.template_response(self.base_template, self.get_context())

    @filter_hook
    def get_breadcrumb(self):
        return [{'url': self.get_admin_url('index'), 'title': 'Accueil'},
                {'url': self.get_admin_url('statistiques'), 'title': 'Statistique'},
                {'url': self.get_admin_url('stats_piel'), 'title': 'Statistique PIEL'}]


xadmin.site.register_view(r'^extraction/$', ExtractionPiel, 'extraction')


class ExtrationPalView(BaseAdminView):

    def get(self, request, *args, **kwargs):
        cod_etp = kwargs.get('step', '')
        step = SettingsEtape.objects.get(cod_etp=cod_etp)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('etudiant')
        queryset = step.wish_set.filter(annee__cod_anu=2014, is_reins=False).order_by('individu__last_name')
        ws.write(1, 0, "code etudiant")
        ws.write(1, 1, "nom")
        ws.write(1, 2, "prenom")
        ws.write(1, 3, "code_dossier")
        ws.write(1, 4, "email")
        ws.write(1, 5, "moyenne generale")
        ws.write(1, 6, "note memoire")
        ws.write(1, 7, "note stage")
        for row, wish in enumerate(queryset):
            ws.write(row+2, 0, wish.individu.student_code)
            ws.write(row + 2, 1, wish.individu.last_name)
            ws.write(row + 2, 2, wish.individu.first_name1)
            ws.write(row + 2, 3, wish.code_dossier)
            ws.write(row + 2, 4, wish.individu.personal_email)
            try:
                ws.write(row + 2, 5, wish.notemastermodel.moyenne_general)
                ws.write(row + 2, 6, wish.notemastermodel.note_memoire)
                ws.write(row + 2, 7, wish.notemastermodel.note_stage)
            except NoteMasterModel.DoesNotExist:
                pass

        response = HttpResponse(mimetype='application/vnd.ms-excel')
        date = datetime.datetime.today().strftime('%d-%m-%Y')
        response['Content-Disposition'] = 'attachment; filename=%s_%s.xls' % ('extraction', date)
        wb.save(response)
        return response

xadmin.site.register_view(r'^extraction_note_view/(?P<step>\w+)/$', ExtrationPalView, 'extraction_note')
