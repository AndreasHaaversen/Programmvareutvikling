from django.urls import path, re_path

from . import views

app_name = 'takeaway'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('checkout/', views.order_create, name='order_create'),
    path('thankyou/<int:pk>', views.ThankYouView.as_view(), name='thankyou'),
    path('search/', views.SearchView.as_view(), name='search'),
]
