from django.urls import reverse
from django.http.response import JsonResponse
from django.views.generic import TemplateView,View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomedAuthenticationForm
from django.core import serializers
from .models import *

# Create your views here.

class CustomedLoginView(LoginView):
     form_class=CustomedAuthenticationForm

class MainPanelView(LoginRequiredMixin,TemplateView):
    template_name="main_panel.html"

    def get_login_url(self):
        return reverse("login")
    
class MenuView(View):
    def get(self,request,*args,**kwargs):
        menu=request.user.role.modules.all()
        print("*****************")
        print(menu)

        menu_data=serializers.serialize("json",menu)
        return JsonResponse({"menu":menu_data},status=200)

