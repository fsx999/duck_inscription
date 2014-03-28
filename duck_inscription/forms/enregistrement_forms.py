# coding=utf-8
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from registration.forms import RegistrationFormTermsOfService
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
import floppyforms as forms


attrs_dict = {'class': 'required'}
from django.forms.util import ErrorList


class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return u''
        return u'<span>%s</span>' % ''.join([u'<span class="help-inline">%s</span>' % e for e in self])


class EmailRegistrationForm(RegistrationFormTermsOfService):
    """
    C'est la classe utilisée pour l'enregistrement d'un compte.
    Warning :
    l'username : ^\w+$ regex
    """
    error_css_class = 'error'
    required_css_class = 'required'
    # captcha = CaptchaField(
    #     label=u"Preuve humaine :",
    #     help_text=u"(Veuillez saisir le mot dans l'image)",)
    username = forms.RegexField(regex=r'^\w+$',
                                help_text=u"(Votre identifiant doit contenir au moins 5 caratères)",
                                min_length=5,
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_(u"Identifiant :"),
                                error_messages={
                                'invalid': u"Ce champ ne doit contenir que des lettres,"
                                           u" des chiffres et des underscores ( _ )."})

    email = forms.EmailField(label=u"E-mail :", help_text=_(u'(Renseignez une adresse électronique valide)'),
                             max_length=100, required=True)
    email1 = forms.EmailField(label=u"Vérification e-mail :", help_text=_(u'(Confirmez l\'adresse électronique)'),
                              max_length=100)
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label=u'Mot de passe :',
        max_length=100,
        help_text=u"(Choisissez un mot de passe personnel)"
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label=u"Vérification mot de passe :",
        max_length=100,
        required=True,
        help_text=u"(Confirmer votre choix de mot de passe)"
    )

    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=u"J'ai lu, compris et j'accepte",
                             error_messages={'required': _(u"Vous devez accepter les conditions d'utilisations")})

    def __init__(self, *args, **kwargs):
        super(EmailRegistrationForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            if self.fields[key].required:
                self.fields[key].widget.attrs['class'] = 'required'

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                _("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']

    def clean(self):
        data = self.cleaned_data
        if data.get('email', '') != '' and data.get('email1', '') != '':
            if data['email'] != data['email1']:
                raise forms.ValidationError(_("Les deux adresses emails ne sont pas identiques"))
        if 'password1' in data and 'password2' in data:

            if data['password1'] != data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class LoginIED(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Saisissez un identifiant et un mot de passe valides. Remarquez que chacun de ces champs est"
                           " sensible à la casse (différenciation des majuscules/minuscules)."),
        'inactive': _("This account is inactive."),
    }


class PasswordRest(PasswordResetForm):
    captcha = CaptchaField(label="Veuillez saisir le mot dans l'image",
                           help_text="(respectez les majuscules et les minuscules)")
    email = forms.EmailField(label="Entrez l'adresse e-mail de votre inscription :", max_length=75)

    # class Media:
    #     js = ("js/password_reset.js",)
    #
    # def __init__(self, *args, **kwargs):
    #     self.helper = FormHelper()
    #     self.helper.form_action = ""
    #     self.helper.form_method = 'POST'
    #     self.helper.form_class = "form-horizontal well"
    #     self.helper.form_id = "form"
    #     self.helper.add_input(Submit("Enregistrer", 'Enregistrer', css_class="btn-success register"))
    #     self.helper.layout = Layout(
    #         'email',
    #         'captcha'
    #     )
    #
    #     super(PasswordRest, self).__init__(*args, **kwargs)
    #     for key in self.fields:
    #         if self.fields[key].required:
    #             self.fields[key].widget.attrs['class'] = 'required'
