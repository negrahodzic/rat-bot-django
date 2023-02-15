import allauth.account.views
from django.conf.urls.static import static
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ratbotwebsite import settings

from . import views
from .views import ResultsListCreateView, ResultsRetrieveUpdateDestroyView

urlpatterns = [
    path('', views.index, name='home'),
    path('leaderboards/', views.leaderboards_page, name='leaderboards'),
    path('results/<int:pk>/', views.results_detail, name='results_detail'),
    path('account/logout', allauth.account.views.logout, name='logout'),
    path('account/login', allauth.account.views.login, name='login'),
    path('oauth2', views.oauth2, name='oauth2'),
    path('api/oauth2/user', views.get_authenticated_user, name='get_authenticated_user'),
    path('api/oauth2/login', views.discord_login, name='oauth2_login'),
    path('api/oauth2/login/redirect', views.discord_login_redirect, name='discord_login_redirect'),
    path('login', views.login_btn, name='login'),
    path('statistics', views.statistics_page, name='statistics'),
    path('api/results', ResultsListCreateView.as_view(), name='results_list_create'),
    path('api/results/<int:pk>', ResultsRetrieveUpdateDestroyView.as_view(), name='results_retrieve_update_destroy'),
    path('api/ratbot_results', views.ratbot_results_api, name='ratbot_results_api'),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
