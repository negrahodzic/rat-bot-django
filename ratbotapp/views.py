from pprint import pprint
import os.path

from django.core.exceptions import ValidationError
from django.db.models import Sum, Max, F
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from requests import Response
from rest_framework import generics, status
from rest_framework.utils import json

from ratbotwebsite.settings import BASE_DIR
from .models import Result, Score, Server, Team
from .serializers import ResultsSerializer
from rest_framework import viewsets

from .models import Membership, Server, Result, Team, Score
from .serializers import MembershipSerializer, ServerSerializer, ResultSerializer, TeamSerializer, ScoreSerializer


# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'ratbot/home.html', {
        'test': "Testing"
    })


auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1039941503423889548&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify"


# auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1039941503423889548&redirect_uri=https%3A%2F%2Frat-bot.up.railway.app%2Fapi%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify"

# @csrf_protect
@csrf_exempt
@login_required(login_url="/api/oauth2/login")
def get_authenticated_user(request: HttpRequest):
    print("======== STARTED get_authenticated_user() =======")
    user = request.user
    return JsonResponse({
        "msg": "Hello! You are authenticated!",
        "id": user.id,
        "discord_tag": user.discord_tag
    })


def oauth2(request: HttpRequest) -> JsonResponse:
    print("======== STARTED oauth2() =======")
    return JsonResponse({"msg": "Hello msg json!"})


# @csrf_protect
@csrf_exempt
def discord_login(request: HttpRequest):
    print("======== STARTED discord_login() =======")
    return redirect(auth_url_discord)


# @csrf_protect
@csrf_exempt
def discord_login_redirect(request: HttpRequest):
    print("======== STARTED discord_login_redirect() =======")
    code = request.GET.get('code')
    pprint(code)
    csrf_token = request.COOKIES.get('csrftoken')
    user = exchange_token(code, csrf_token)
    pprint(user)
    discord_user = authenticate(request, user=user)
    pprint(discord_user)
    discord_user = list(discord_user).pop()
    login(request, discord_user)

    headers = {
        "X-CSRFToken": csrf_token
    }
    return redirect("/api/oauth2/user", headers=headers)
    # return redirect("/api/oauth2/user")


def exchange_token(code: str, csrf_token: str):
    print("======== STARTED exchange_token() =======")
    data = {
        "client_id": "1039941503423889548",
        "client_secret": "YvjOBw2O3jsmfeA5JfiMfSaeJguA03rW",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": str(BASE_DIR) + "/api/oauth2/login/redirect"
    }

    print(str(BASE_DIR) + "/api/oauth2/login/redirect")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrf_token
    }

    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    credentials = response.json()
    print(credentials)
    access_token = credentials['access_token']
    response = requests.get("https://discord.com/api/v6/users/@me", headers={
        "Authorization": 'Bearer %s' % access_token,
        "X-CSRFToken": csrf_token
    })
    user = response.json()
    pprint(user)
    return user


# @csrf_protect
@csrf_exempt
def login_btn(request: HttpRequest):
    print("======== STARTED login_btn() =======")
    # return redirect("/api/oauth2/login")
    return redirect("/accounts/discord/login")


@csrf_exempt
@login_required(login_url="/accounts/discord/login")
def teams(request):
    print("======== STARTED teams() =======")
    data = Team.objects.all()
    return render(request, 'ratbot/teams.html', {
        'teams': data
    })


# @csrf_protect
@csrf_exempt
@login_required(login_url="/accounts/discord/login")
# @login_required(login_url="/accounts/login")
def leaderboards_page(request):
    print("======== STARTED leaderboards_page() =======")
    print(str(BASE_DIR) + "/api/oauth2/login/redirect")
    results = Result.objects.all()
    return render(request, 'ratbot/leaderboards.html', {
        'results': results
    })


def results_detail(request, pk):
    print("======== STARTED result() =======")
    # result = Result.objects.filter(id=id)
    result = get_object_or_404(Result, pk=pk)
    scores = Score.objects.filter(result_id=result.id).order_by('rank')
    context = {'result': result, 'scores': scores}
    pprint(result)
    pprint(scores)
    return render(request, 'ratbot/results_detail.html', context)


@login_required(login_url="/accounts/discord/login")
def statistics_page(request):
    print("======== STARTED statistics_page() =======")
    # results = Result.objects.all()
    #
    # top_scores = Score.objects.values("result_id").annotate(
    #     max_tp=Max("tp")
    # ).order_by("-max_tp")[:3]
    #
    # top_results = Result.objects.filter(id__in=[score["result_id"] for score in top_scores])

    # top_scores = Score.objects.values("result_id__server_name").annotate(
    #     max_tp=Max("tp")
    # ).order_by("-max_tp")
    #
    # top_results = []
    # for score in top_scores:
    #     result = Result.objects.filter(server_name=score["result_id__server_name"],
    #                                    date_played=score["result_id__date_played"]).first()
    #     score_object = Score.objects.filter(result=result, tp=score["max_tp"]).first()
    #     top_results.append({"result": result, "score": score_object})
    #
    # top_stats = top_results

    top_stats = Score.objects.filter(tp__gte=0).order_by('-tp').select_related('result')[:3]

    context = {
        'statistics': {
            # 'top_results': top_results,
            # 'top_scores': top_scores,
            'top_stats': top_stats
        }
    }

    pprint(context)
    # pprint(top_stats[0].result.server_name)

    return render(request, 'ratbot/statistics.html', context)


class ResultsListCreateView(generics.ListCreateAPIView):
    print('ResultsListCreateView')
    queryset = Result.objects.all()
    serializer_class = ResultsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ResultsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    print('ResultsRetrieveUpdateDestroyView')
    queryset = Result.objects.all()
    serializer_class = ResultsSerializer


from django.utils import timezone


@csrf_exempt
def ratbot_results_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'})

    try:
        final_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'})

    # Extract relevant data from final_data
    server_data = final_data.get('server', {})
    result_data = final_data.get('result', {})
    scores_data = final_data.get('scores', [])

    # Get the guild_id and guild_name values from server_data
    guild_id = server_data.get('guild_id')
    guild_name = server_data.get('guild_name')

    # Raise an exception if guild_name is not provided or is an empty string
    if not guild_name:
        raise ValueError("Guild name is required!")
    if not isinstance(guild_name, str):
        raise ValueError("Guild name should be a string.")

    # Get the existing server instance if it already exists
    try:
        server = Server.objects.get(guild_id=guild_id)
    except Server.DoesNotExist:
        server = None

    # Create or update the server instance if it doesn't exist or if guild_name has changed
    if server is None or server.guild_name != guild_name:
        server, server_created = Server.objects.update_or_create(
            guild_id=guild_id,
            defaults={
                'guild_name': guild_name
            }
        )
        print(f"Server created or updated? {'created' if server_created else 'updated'}")

    # Check if all required result data fields are present and of the expected type
    required_result_fields = {
        'generated_by': str,
        'scrim_name': str,
        'date_played': str,
        'time_played': str,
    }
    for field, field_type in required_result_fields.items():
        if not result_data.get(field):
            raise ValueError(f"{field} is required!")
        if not isinstance(result_data.get(field), field_type):
            raise ValueError(f"{field} should be a {field_type.__name__}.")

    # Check if a result with the same server, scrim name, and date already exists
    result = Result.objects.filter(
        server=server,
        scrim_name=result_data.get('scrim_name'),
        date_played=result_data.get('date_played'),
        time_played=result_data.get('time_played')
    ).first()

    if result:
        # Update the existing result
        result.generated_by = result_data.get('generated_by')
        result.scrim_type = Result.ScrimType.OPEN
        result.save()
    else:
        try:
            # Create a new Result instance
            result = Result.objects.create(
                generated_by=result_data.get('generated_by'),
                server=server,
                scrim_name=result_data.get('scrim_name'),
                scrim_type=Result.ScrimType.OPEN,
                date_played=result_data.get('date_played') or timezone.now().date(),
                time_played=result_data.get('time_played')
            )
        except ValidationError as e:
            # Handle validation error
            print("Validation Error: ", e.message)
        except Exception as e:
            # Handle other exceptions
            print("Error: ", e)

    # Create Score instances
    print()
    scores = []
    for score_data in scores_data:
        team_name = score_data.get('team_name')
        team_tag = score_data.get('team_tag')
        team, _ = Team.objects.get_or_create(
            team_name=team_name,
            defaults={
                'team_tag': team_tag
            }
        )
        # Check if a score with the same rank already exists for this result
        existing_score = Score.objects.filter(
            result=result,
            rank=score_data.get('rank')
        ).first()
        if existing_score:
            # Update the existing score
            existing_score.team = team
            existing_score.wwcd = score_data.get('wwcd')
            existing_score.pp = score_data.get('pp')
            existing_score.kp = score_data.get('kp')
            existing_score.tp = score_data.get('tp')
            existing_score.missed_games = score_data.get('missed_games')
            existing_score.save()
        else:
            # Create a new Score instance
            score = Score(
                result=result,
                team=team,
                rank=score_data.get('rank'),
                wwcd=score_data.get('wwcd'),
                pp=score_data.get('pp'),
                kp=score_data.get('kp'),
                tp=score_data.get('tp'),
                missed_games=score_data.get('missed_games')
            )
            # score.save()
            scores.append(score)

    Score.objects.bulk_create(scores)

    return JsonResponse({'success': 'Result saved successfully'})


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    http_method_names = ['get']


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    http_method_names = ['get']


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    http_method_names = ['get']


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    http_method_names = ['get']


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    http_method_names = ['get']


class MembershipList(generics.ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class MembershipDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class ServerList(generics.ListCreateAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class ServerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class ResultList(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class ResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class ScoreList(generics.ListCreateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer


class ScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
