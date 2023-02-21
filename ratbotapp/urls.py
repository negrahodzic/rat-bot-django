import allauth.account.views
from django.conf.urls.static import static
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ratbotwebsite import settings
from django.urls import re_path
from django.views.generic import RedirectView
from django.urls import path
from .views import MembershipList, MembershipDetail, ServerList, ServerDetail, ResultList, ResultDetail, TeamList, TeamDetail, ScoreList, ScoreDetail
from .views import MembershipViewSet, ServerViewSet, ResultViewSet, TeamViewSet, ScoreViewSet

from . import views
from .views import ResultsListCreateView, ResultsRetrieveUpdateDestroyView

urlpatterns = [
    path('', views.index, name='home'),
    path('teams', views.teams, name='teams'),
    path('leaderboards', views.leaderboards_page, name='leaderboards'),
    path('results/<int:pk>', views.results_detail, name='results_detail'),
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
    # re_path(r'^.*$', RedirectView.as_view(url='/')),
    path('api/memberships/', MembershipViewSet.as_view({'get': 'list'}), name='membership-list'),
    path('api/memberships/<int:pk>/', MembershipViewSet.as_view({'get': 'retrieve'}), name='membership-detail'),
    path('api/servers/', ServerViewSet.as_view({'get': 'list'}), name='server-list'),
    path('api/servers/<int:pk>/', ServerViewSet.as_view({'get': 'retrieve'}), name='server-detail'),
    path('api/results/', ResultViewSet.as_view({'get': 'list'}), name='result-list'),
    path('api/results/<int:pk>/', ResultViewSet.as_view({'get': 'retrieve'}), name='result-detail'),
    path('api/teams/', TeamViewSet.as_view({'get': 'list'}), name='team-list'),
    path('api/teams/<int:pk>/', TeamViewSet.as_view({'get': 'retrieve'}), name='team-detail'),
    path('api/scores/', ScoreViewSet.as_view({'get': 'list'}), name='score-list'),
    path('api/scores/<int:pk>/', ScoreViewSet.as_view({'get': 'retrieve'}), name='score-detail'),


]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
