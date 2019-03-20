from django.urls import path, re_path

from . import views

app_name = 'takeaway'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    re_path(r'^(?P<search>.*)/$', views.SearchView.as_view(), name = 'index2'),
    path('checkout/', views.order_create, name='order_create'),
    path('thankyou/<int:pk>', views.ThankYouView.as_view(), name='thankyou'),
]
