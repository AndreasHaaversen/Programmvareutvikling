from django.shortcuts import redirect


def takeawayredirect(request):
    return redirect('/takeaway', permanent=True)
