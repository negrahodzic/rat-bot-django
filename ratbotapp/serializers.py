from rest_framework import serializers
from .models import Membership, Server, Result, Team, Score


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):
    membership = MembershipSerializer()

    class Meta:
        model = Server
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    server = ServerSerializer()

    class Meta:
        model = Result
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class ScoreSerializer(serializers.ModelSerializer):
    result = ResultSerializer()
    team = TeamSerializer()

    class Meta:
        model = Score
        fields = '__all__'
