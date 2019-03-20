from django.urls import path

from . import views

app_name = 'employeepanel'
urlpatterns = [
    path('', views.employeeredirect, name='index'),
    path('active_orders/', views.ActiveOrderView.as_view(),
         name='active_orders'),
    path('cancelled_orders/', views.CancelledOrderView.as_view(),
         name='cancelled_orders'),
    path('collected_orders/', views.CollectedOrderView.as_view(),
         name='collected_orders'),
	path('order/<int:pk>/edit/', views.EditOrderView.as_view(),
         name='edit_order'),
	path('order/<int:pk>/edititem/', views.EditOrderItemView.as_view(),
         name='edit_order'),
    path('update_order/<int:pk>', views.update_order_status,
         name='update_order'),
]
