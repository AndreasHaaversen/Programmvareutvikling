from django.shortcuts import render
from django.views import generic
from .models import Dish
from .forms import OrderForm


class IndexView(generic.ListView, generic.FormView):
    template_name = 'takeaway/index.html'
    context_object_name = 'dish_list'

    form_class = OrderForm
    success_url = "takeaway/thankyou.html"

    def get_queryset(self):
        return Dish.objects.order_by('dish_type')

    def add_order(request):
        self.object = self.get_object()
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('takeaway/thankyou.html')
        else:
            form = OrderForm()
            return render(request, 'takeaway/index.html', {'form': form})
