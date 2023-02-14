from pprint import pprint
import os.path

from django.db.models import Sum, Max, F
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework import generics

from ratbotwebsite.settings import BASE_DIR
from .models import Result, Score
from .serializers import ResultsSerializer


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


class ResultsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    print('ResultsRetrieveUpdateDestroyView')
    queryset = Result.objects.all()
    serializer_class = ResultsSerializer
