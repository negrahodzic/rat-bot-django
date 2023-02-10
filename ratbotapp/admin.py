from django.contrib import admin
# from ratbotapp.models import DiscordUser

from .models import Result, Score, DiscordUser

# Register your models here.

admin.site.register(DiscordUser)
admin.site.register(Result)
admin.site.register(Score)
