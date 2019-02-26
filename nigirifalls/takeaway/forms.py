import datetime

from django import forms
from .models import OrderInfo, Dish
from django.utils import timezone


class OrderCreateForm(forms.ModelForm):

    def clean_pickup_time(self):
        data = self.cleaned_data['pickup_time']
        if timezone.now() + datetime.timedelta(minutes=30) > data:
            raise forms.ValidationError(
                "Pickup time must be at least 30 minutes into the future!"
            )
        return data

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if data < 10000000 or data > 99999999:
            raise forms.ValidationError(
                "Phone numbers must be 8 digits long"
            )
        return data

    class Meta:
        model = OrderInfo
        widgets = {
            'pickup_time': forms.DateTimeInput(
                {'placeholder': 'YYYY-MM-DD HH:mm'}
            )
        }
        fields = ['name_of_customer', 'email', 'phone_number',
                  'pickup_time', 'comment', ]
