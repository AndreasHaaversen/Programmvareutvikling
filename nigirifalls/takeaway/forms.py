from django import forms
from .models import OrderInfo


class OrderForm(forms.ModelForm):

    class Meta:
        model = OrderInfo
        fields = ['name_of_customer', 'phone_number',
                  'pickup_time', 'comment']
