from django.contrib import admin

from .models import Result, Score, DiscordUser, Team, Membership, Server

# Register your models here.
admin.site.register(Server)
admin.site.register(Membership)
admin.site.register(DiscordUser)
admin.site.register(Result)
admin.site.register(Score)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_tag', 'team_slug')
    readonly_fields = ('team_slug',)


admin.site.register(Team, TeamAdmin)
