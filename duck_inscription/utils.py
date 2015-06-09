# coding=utf-8
from __future__ import unicode_literals
from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import available_attrs


def user_passes_test(test_func):
    """
    decorateur copier de django et modifié
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_anonymous():
                return redirect('/')
            pk = kwargs.get('pk', '')
            if request.user.is_staff:
                return view_func(request, *args, **kwargs)
            if request.path_info in ["/individu/recapitulatif/{}/modif_individu".format(pk),
                                     "/individu/recapitulatif/{}/modif_adresse".format(pk)]:
                if request.user.individu.get_absolute_url() != reverse('recap', kwargs={'pk': pk}):
                    return redirect(request.user.individu.get_absolute_url())
                else:
                    return view_func(request, *args, **kwargs)
            if test_func(request.user) and request.path_info == request.user.individu.get_absolute_url():
                return view_func(request, *args, **kwargs)


            return redirect(request.user.individu.get_absolute_url())

        return _wrapped_view

    return decorator


def user_verif_etape_and_login(function=None):
    """
    Ce décorateur permet de faire une vérification si l'utilisateur est bien logué
    et si l'étape de l'individu est bien l'étape demandé (pour éviter de venir par url)
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated()

    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def wish_passes_test(test_func):
    """
    decorateur copier de django et modifié
    """
    from duck_inscription.models import Wish

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_anonymous():
                return redirect('/')
            if request.user.is_staff:
                return view_func(request, *args, **kwargs)
            if test_func(request.user) and request.user.individu.get_absolute_url() == reverse('accueil', kwargs={'pk': request.user.individu.pk}):  # l'individu est bien authentifié et il a fini
                try:  # si l'étudiant à un voeu
                    wish = request.user.individu.wishes.get(pk=kwargs['pk'])
                    if request.path_info == wish.get_absolute_url():  # c'est la bonne url
                        return view_func(request, *args, **kwargs)
                    else:
                        return redirect(wish.get_absolute_url())
                except (Wish.DoesNotExist, KeyError), e:  # il n'a pas de voeux
                    if request.path_info != reverse("new_wish", kwargs={'pk': request.user.individu.pk}):
                        return redirect(reverse('accueil', kwargs={'pk': request.user.individu.pk}))
                return view_func(request, *args, **kwargs)


            return redirect(reverse('accueil'), kwargs={'pk': request.user.individu.pk})

        return _wrapped_view

    return decorator


def wish_verif_etape_and_login(function=None):
    actual_decorator = wish_passes_test(
        lambda u: u.is_authenticated()

    )
    if function:
        return actual_decorator(function)
    return actual_decorator




def verif_ine(ine):
    """
    :param ine: String de 11 caractère compris [A-Z1-9]
    :return: un Boolean pour vrai faux
    :exception: TypeError et ValueError si ine malformé (avec espace ou bien des accents
    """
    try:
        if len(ine) < 11:
            return False
        ine = ine.upper()
        if ine[-1].isdigit():
            return verif_cle_ine(ine)
        else:
            return verif_cle_bea(ine)
    except (TypeError, ValueError):
        return False


def verif_cle_bea(ine):
    if ine[-1].isdigit():
        return False
    ref = "ABCDEFGHJKLMNPRSTUVWXYZ"
    big = int(ine[:-1])
    div = 23.0
    res1 = big/23
    ent = int(res1)
    res2 = ent * div
    val = big - res2
    cle = int(val)
    return ref[cle] == ine[-1]


def verif_cle_ine(ine):
        # if len(ine) < 11:
        #     return "mauvaise longeur"
        tab = [''] * 10
        arg_cle = ine[-1]  # récupére la clé

        for i in range(0, 10):
            if ine[i].isdigit():
                tab[i] = int(ine[i])
            else:
                tab[i] = int(place(ine[i]))
        clef = 0
        for i in range(0, 9):
            if tab[i] != 0:
                plus = tab[i] * 6
                clef += plus

        clef += int(tab[-1])

        str1 = str(clef)
        lg = len(str1)
        new_cle = str1[-1]
        if arg_cle == new_cle:
            return True
        else:
            return False


def place(arg):
    ref = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for j in range(0, 26):
        if arg == ref[j]:
            return j + 10
