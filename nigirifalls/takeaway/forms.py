from django import forms
from .models import OrderInfo, Dish


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = OrderInfo
        fields = ['name_of_customer', 'email', 'phone_number',
                  'pickup_time', 'comment', ]
