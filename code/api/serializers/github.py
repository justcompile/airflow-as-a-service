from rest_framework import serializers


class GitRepo(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    private = serializers.BooleanField()
    url = serializers.URLField(source='html_url')
    language = serializers.CharField()
    selected = serializers.BooleanField()
