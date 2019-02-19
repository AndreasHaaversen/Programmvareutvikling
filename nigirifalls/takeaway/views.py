from django.shortcuts import render
from django.views import generic
from .models import Dish


class IndexView(generic.ListView):
    template_name = 'takeaway/index.html'
    context_object_name = 'dish_list'

    def get_queryset(self):
        return Dish.objects.order_by('dish_type')
