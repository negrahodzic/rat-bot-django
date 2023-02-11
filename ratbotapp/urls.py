from pprint import pprint

import allauth.account.views
from django.urls import path

from ratbotwebsite import settings
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='home'),
    path('leaderboards/', views.leaderboards_page, name='leaderboards'),
    path('result/<int:pk>/', views.result, name='result'),
    path('account/logout', allauth.account.views.logout, name='logout'),
    path('account/login', allauth.account.views.login, name='login'),
    path('oauth2', views.oauth2, name='oauth2'),
    path('api/oauth2/user', views.get_authenticated_user, name='get_authenticated_user'),
    path('api/oauth2/login', views.discord_login, name='oauth2_login'),
    path('api/oauth2/login/redirect', views.discord_login_redirect, name='discord_login_redirect'),
    path('login', views.login_btn, name='login'),
    path('test', views.test, name='test')
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
pprint(urlpatterns)
