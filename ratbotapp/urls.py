import allauth.account.views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView

from ratbotwebsite import settings
from django.urls import path, re_path
from .views import ResultViewSet, TeamViewSet, CodashopView, generate_token

from . import views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# import your views here

team_list = TeamViewSet.as_view({'get': 'list'})
team_detail = TeamViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    path('', views.index, name='home'),
    path('api', views.api_info, name='api-info'),
    path('teams', views.teams, name='teams'),
    path('teams/<int:pk>', views.team_detail, name='team_detail'),
    path('teams/<int:team_id>/follow/', views.follow_team, name='follow_team'),
    path('teams/<int:team_id>/unfollow/', views.unfollow_team, name='unfollow_team'),

    path('leaderboards', views.leaderboards_page, name='leaderboards'),
    path('results/<int:pk>', views.results_detail, name='results_detail'),
    path('my_account/', views.my_account, name='my_account'),
    path('my_account/generate_token/', views.generate_token, name='generate_token'),
    path('my_account/delete_token/', views.delete_token, name='delete_token'),
    path('account/logout', allauth.account.views.logout, name='logout'),
    path('account/login', allauth.account.views.login, name='login'),
    path('oauth2', views.oauth2, name='oauth2'),
    path('api/oauth2/user', views.get_authenticated_user, name='get_authenticated_user'),
    path('api/oauth2/login', views.discord_login, name='oauth2_login'),
    path('api/oauth2/login/redirect', views.discord_login_redirect, name='discord_login_redirect'),
    path('login', views.login_btn, name='login'),
    path('statistics', views.statistics_page, name='statistics'),
    path('api/ratbot_results', views.ratbot_results_api, name='ratbot_results_api'),
    # path('api/results/', ResultViewSet.as_view({'get': 'list'}), name='result-list'),
    # path('api/results/<int:pk>/', ResultViewSet.as_view({'get': 'retrieve'}), name='result-detail'),
    path('api/teams/', TeamViewSet.as_view({'get': 'list'}), name='team-list'),
    path('api/teams/<int:pk>/', TeamViewSet.as_view({'get': 'retrieve'}), name='team-detail'),
    path('api/codashop/', CodashopView.as_view(), name='codashop'),
    # re_path(r'^.*$', RedirectView.as_view(url='/')),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add the authentication classes and permission classes to the viewsets
TeamViewSet.authentication_classes = [TokenAuthentication]
TeamViewSet.permission_classes = [IsAuthenticated]
