from django.urls import path

from . import views

app_name = 'takeaway'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('checkout/', views.order_create, name='order_create'),
    path('thankyou/<int:pk>', views.ThankYouView.as_view(), name='thankyou'),
    path('admin/order/<int:order_id>/pdf/',
         views.create_order_pdf,
         name='create_order_pdf'),
]
