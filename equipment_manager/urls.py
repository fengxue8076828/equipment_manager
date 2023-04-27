"""equipment_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from info_manager.views import MainPanelView,MenuView,CustomedLoginView,UserProfileView,PasswordChangeView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',CustomedLoginView.as_view(),name="login"), 
    path('logout/',LogoutView.as_view(),name="logout"), 
    path('',MainPanelView.as_view(),name="main_panel"), 
    path('menu/',MenuView.as_view(),name="menu"),
    path('user-profile/',UserProfileView.as_view(),name="user-profile"),
    path('user-password/',PasswordChangeView.as_view(),name="user-password"),
    path('info-manager/',include("info_manager.urls",namespace="info_manager")),
    path('presale/',include("presale.urls",namespace="presale")),
    path('postsale/',include("postsale.urls",namespace="postsale")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
