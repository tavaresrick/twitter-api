from django.urls import include, path

from . import views

urlpatterns = [
    path('v1/users', views.TopUsersView.as_view()),
    path('v1/hour', views.ByHourView.as_view()),
    path('v1/tags', views.ByTagCountryLanguageView.as_view()),
    path('v1/populate', views.PopulateView().as_view()),
    path('health', views.health_check, name='health_check'),
]