from django.views import generic
from takeaway.models import OrderInfo, OrderItem
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.urls import reverse
from django.views.generic.edit import UpdateView, FormView, CreateView
from django.views.decorators.http import require_POST
from takeaway.mail import send_order_email_with_pdf, send_email
from .forms import UpdateOrderStatusForm, OrderUpdateForm, OrderUpdateQuantityForm, AddOrderItemForm
from django.utils import timezone
import datetime
from django.contrib import messages


def employeeredirect(request):
    return redirect(reverse("employeepanel:active_orders"))


class GenericOrderView(generic.ListView):
    template_name = 'employeepanel/index.html'
    context_object_name = 'order_list'

    def get_context_data(self):
        context = super().get_context_data()
        context['update_order_status_form'] = UpdateOrderStatusForm()
        return context


class CancelledOrderView(GenericOrderView):
    def get_context_data(self):
        context = super().get_context_data()
        context['viewtype'] = 'Cancelled orders'
        return context

    def get_queryset(self):
        return OrderInfo.objects.filter(status="cancelled")


class ActiveOrderView(GenericOrderView):
    def get_context_data(self):
        context = super().get_context_data()
        context['viewtype'] = 'Active orders'
        return context

    def get_queryset(self):
        return OrderInfo.objects.exclude(
            status="cancelled").exclude(
            status="collected").order_by('pickup_time')


class CollectedOrderView(GenericOrderView):
    def get_context_data(self):
        context = super().get_context_data()
        context['viewtype'] = 'Collected orders'
        return context

    def get_queryset(self):
        return OrderInfo.objects.filter(status="collected")

class EditOrderView(UpdateView):
    model = OrderInfo
    form_class = OrderUpdateForm
    template_name = 'employeepanel/orderedit.html'


class EditOrderItemView(UpdateView):
    model = OrderItem
    form_class = OrderUpdateQuantityForm
    template_name = 'employeepanel/orderedit.html'


class AddOrderItemView(CreateView):
    model = OrderItem
    form_class = AddOrderItemForm
    template_name = 'employeepanel/orderedit.html'

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

        if cd['status'] == 'cancelled':
            send_order_email_with_pdf(
                order,
                "Please find attached order cancellation confirmation.\n\nSincerely,\nThe Nigiri Falls team"
            )

        if cd['status'] == 'ready':
            send_email(
                order,
                "Your order nr. {} is ready to be picked up!\n\nSincerely,\nThe Nigiri Falls team".format(order.id)
            )

    return redirect(reverse('employeepanel:active_orders'))
