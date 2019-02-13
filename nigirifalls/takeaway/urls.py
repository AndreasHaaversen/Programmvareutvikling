from django.urls import path

from . import views

app_name = 'takeaway'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]