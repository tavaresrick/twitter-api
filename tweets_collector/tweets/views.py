from django.http import HttpResponse
from tweets.models import TweetManager
from rest_framework import views
from rest_framework.response import Response
from http import HTTPStatus

from .serializers import TopUsersSerializer, ByHourSerializer, ByTagCountryLanguageSerializer
from .utils import health_check_full

class TopUsersView(views.APIView):
    def get(self, request):
        users = TweetManager.top_users()
        results = TopUsersSerializer(users, many=True).data
        return Response(results)

class ByHourView(views.APIView):
    def get(self, request):
        posts = TweetManager.by_hour()
        results = ByHourSerializer(posts, many=True).data
        return Response(results)

class ByTagCountryLanguageView(views.APIView):
    def get(self, request):
        tag = TweetManager.by_tag_country_language()
        results = ByTagCountryLanguageSerializer(tag, many=True).data
        return Response(results)

class PopulateView(views.APIView):
    def post(self, request):
        if TweetManager.populate():
            return HttpResponse("",content_type="application/json",status=HTTPStatus.CREATED)
        return HttpResponse("",content_type="application/json",status=HTTPStatus.INTERNAL_SERVER_ERROR)

def health_check(request):
    if health_check_full():
        return HttpResponse("",content_type="application/json",status=HTTPStatus.OK)
    return HttpResponse("",content_type="application/json",status=HTTPStatus.INTERNAL_SERVER_ERROR)
