from rest_framework import serializers

class TopUsersSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    followers = serializers.IntegerField(read_only=True, source='followers__max')

class ByHourSerializer(serializers.Serializer):
    date = serializers.DateTimeField(read_only=True)
    count = serializers.IntegerField(read_only=True, source='total')

class ByTagCountryLanguageSerializer(serializers.Serializer):
    tag = serializers.CharField(read_only=True)
    country = serializers.CharField(read_only=True, required=False)
    language = serializers.CharField(read_only=True, required=False)
    count = serializers.IntegerField(read_only=True, source='tag__count')