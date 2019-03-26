import datetime

from django import forms
from takeaway.models import OrderInfo, Dish
from django.utils import timezone

ORDER_STATUS_CHOICES = (
    ('accepted', 'Accepted'),
    ('prod', 'In production'),
    ('ready', 'Ready'),
    ('collected', 'Collected'),
    ('cancelled', 'Cancelled'),
)


class UpdateOrderStatusForm(forms.ModelForm):
    class Meta:
        model = OrderInfo
        fields = ['status']


class OrderUpdateForm(forms.ModelForm):

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
		
    def clean(self):
        cleaned_data = super(OrderUpdateForm, self).clean()
	    # Remove later if not needed
        pickup_time = cleaned_data.get('pickup_time')

        if self.instance.pickup_time < timezone.now() + datetime.timedelta(minutes=30):
            self.add_error('pickup_time', 'Cannot edit an order after 30 minutes has passed!')

        return cleaned_data

    class Meta:
        model = OrderInfo
        widgets = {
            'pickup_time': forms.DateTimeInput(
                {'placeholder': 'YYYY-MM-DD HH:mm'}
            )
        }
        template_name = 'employeepanel/orderedit.html'
        fields = ['name_of_customer','email','phone_number','pickup_time','comment']