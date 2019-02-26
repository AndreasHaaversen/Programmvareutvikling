from django.shortcuts import redirect
from django.urls import reverse


def takeawayredirect(request):
    return redirect(reverse("takeaway:index"))
