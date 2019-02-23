from django import forms
from .models import OrderInfo, Dish


class OrderForm(forms.ModelForm):

    class Meta:
        model = OrderInfo
        fields = ['name_of_customer', 'phone_number',
                  'pickup_time', 'comment', ]

    def save(self):
        instance = forms.ModelForm.save(self)
        instance.dishes_set.clear()
        instance.dishes_set.add(*self.cleaned_data['dishes'])
        return instance
