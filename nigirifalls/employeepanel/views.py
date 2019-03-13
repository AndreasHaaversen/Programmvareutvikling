from django.views import generic
from takeaway.models import OrderInfo
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from .forms import UpdateOrderStatusForm
from django.utils import timezone
import datetime
from django.contrib import messages


def employeeredirect(request):
    return redirect(reverse("employeepanel:active_orders"))


class CancelledOrderView(generic.ListView):
    template_name = 'employeepanel/index.html'
    context_object_name = 'order_list'

    def get_context_data(self):
        context = super().get_context_data()
        context['update_order_status_form'] = UpdateOrderStatusForm()
        context['viewtype'] = 'Cancelled orders'
        return context

    def get_queryset(self):
        return OrderInfo.objects.filter(status="cancelled")


class ActiveOrderView(generic.ListView):
    template_name = 'employeepanel/index.html'
    context_object_name = 'order_list'

    def get_context_data(self):
        context = super().get_context_data()
        context['update_order_status_form'] = UpdateOrderStatusForm()
        context['viewtype'] = 'Active orders'
        return context

    def get_queryset(self):
        return OrderInfo.objects.exclude(
            status="cancelled").exclude(
            status="collected").order_by('pickup_time')


class CollectedOrderView(generic.ListView):
    template_name = 'employeepanel/index.html'
    context_object_name = 'order_list'

    def get_context_data(self):
        context = super().get_context_data()
        context['update_order_status_form'] = UpdateOrderStatusForm()
        context['viewtype'] = 'Collected orders'
        return context

    def get_queryset(self):
        return OrderInfo.objects.filter(status="collected")


@require_POST
def update_order_status(request, pk):
    order = get_object_or_404(OrderInfo, id=pk)
    form = UpdateOrderStatusForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if cd['status'] == 'cancelled':
            if timezone.now() + datetime.timedelta(minutes=30) < order.pickup_time:
                order.status = cd['status']
            else:
                messages.add_message(
                    request, messages.ERROR, "Can't cancel order if there is less than 30 minutes to pickup time")
        else:
            order.status = cd['status']
        order.save(update_fields=['status'])
    return redirect(reverse('employeepanel:active_orders'))
