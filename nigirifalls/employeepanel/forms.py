from django import forms
from takeaway.models import OrderInfo

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
        labels = {
            'status': 'Set status to'
        }

