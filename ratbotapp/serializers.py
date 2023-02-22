from rest_framework import serializers
from .models import Membership, Server, Result, Team, Score

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):
    membership = MembershipSerializer()

    class Meta:
        model = Server
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['id', 'rank', 'team_managers', 'wwcd', 'pp', 'kp', 'tp']


class ResultSerializer(serializers.ModelSerializer):
    guild_id = serializers.IntegerField(source='server.guild_id')
    guild_name = serializers.CharField(source='server.guild_name')
    scores = ScoreSerializer(many=True, read_only=True)

    class Meta:
        model = Result
        fields = ['id', 'guild_id', 'guild_name', 'generated_by', 'scrim_name', 'date_played', 'time_played', 'scores']

