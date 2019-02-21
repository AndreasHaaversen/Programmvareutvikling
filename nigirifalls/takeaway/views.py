from django.shortcuts import render, reverse
from django.views import generic
from .models import Dish, OrderInfo
from .forms import OrderForm


class IndexView(generic.View):

    def get(self, request, *args, **kwargs):
        view = IndexDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = IndexOrder.as_view()
        return view(request, *args, **kwargs)


class IndexDisplay(generic.ListView):
    template_name = 'takeaway/index.html'

    def get_queryset(self):
        return Dish.objects.order_by('dish_type')

    def get_context_data(self):
        context = super().get_context_data()
        context['form'] = OrderForm()
        return context


class IndexOrder(generic.FormView):
    template_name = 'takeaway/index.html'
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        order_place_form = OrderForm()
        return super.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('thankyou', kwargs={'pk': self.object.pk})


class ThankYouView(generic.DetailView):
    model = OrderInfo
    template_name = 'takeaway/thankyou.html'
