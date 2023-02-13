from django.contrib import admin
# from ratbotapp.models import DiscordUser

from .models import Result, Score, DiscordUser, Team

# Register your models here.

admin.site.register(DiscordUser)
admin.site.register(Result)
admin.site.register(Score)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_tag', 'team_slug')
    readonly_fields = ('team_slug',)


admin.site.register(Team, TeamAdmin)
