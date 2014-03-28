# Create your views here.
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic.base import View


class UserView(View):
    def get(self, request, *args, **kwargs):
        message = "true"
        if User.objects.filter(username=request.GET.get('username', "")).count() != 0:
            message = "false"
        return HttpResponse(message)


class EmailView(View):
    def get(self, request, *args, **kwargs):
        message = "true"
        if User.objects.filter(email=request.GET.get('email', "")).count() != 0:
            message = "false"
        return HttpResponse(message)
