from pprint import pprint

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Result

# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'ratbot/home.html', {
        'test': "Testing"
    })


auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1039941503423889548&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify"


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


def discord_login(request: HttpRequest):
    print("======== STARTED discord_login() =======")
    return redirect(auth_url_discord)


def discord_login_redirect(request: HttpRequest):
    print("======== STARTED discord_login_redirect() =======")
    code = request.GET.get('code')
    pprint(code)
    user = exchange_token(code)
    pprint(user)
    discord_user = authenticate(request, user=user)
    pprint(discord_user)
    discord_user = list(discord_user).pop()
    login(request, discord_user)
    return redirect("/api/oauth2/user")


def exchange_token(code: str):
    print("======== STARTED exchange_token() =======")
    data = {
        "client_id": "1039941503423889548",
        "client_secret": "YvjOBw2O3jsmfeA5JfiMfSaeJguA03rW",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/api/oauth2/login/redirect"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    credentials = response.json()
    print(credentials)
    access_token = credentials['access_token']
    response = requests.get("https://discord.com/api/v6/users/@me", headers={
        "Authorization": 'Bearer %s' % access_token
    })
    user = response.json()
    pprint(user)
    return user


def login_btn(request: HttpRequest):
    print("======== STARTED login_btn() =======")
    # return redirect("/api/oauth2/login")
    return redirect("/accounts/discord/login")

@login_required(login_url="/accounts/discord/login")
def leaderboards_page(request):
    print("======== STARTED leaderboards_page() =======")
    results = Result.objects.all()
    return render(request, 'ratbot/leaderboards.html', {
        'results': results
    })

def result(request, pk):
    print("======== STARTED result() =======")
    result = Result.objects.filter(scrim=pk)
    return render(request, 'ratbot/result.html', {
        'result': result[0]
    })