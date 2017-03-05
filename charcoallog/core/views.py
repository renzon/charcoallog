from django.shortcuts import render
# from django.core.urlresolvers import reverse
# from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# from django.db import IntegrityError, transaction
from django.db.models import Sum
from .models import Extract
from .forms import EditExtractForm, SelectExtractForm
from datetime import date


# Create your views here.
@login_required
def home(request):
    return render(request, "principal.html")


@login_required
def title(request):
    return render(request, "frameset_pages/title.html")


@login_required
def middle(request):
    return render(request, "frameset_pages/middle.html")


@login_required
def rodape(request):
    return render(request, "frameset_pages/rodape.html")


@login_required
def show_data(request):
    user = request.user
    builds = False  # Extract.objects.filter(user_name=user).order_by('date')
    total = False  # Extract.objects.filter(user_name=user).aggregate(Sum('money'))
    d = date.today()
    d = d.strftime('%Y-%m-01')

    if request.method == 'POST':
        form = EditExtractForm(request.POST)

        if form.is_valid():
            Extract.objects.insert_by_post(form)

            # builds = Extract.objects.filter(user_name=user).order_by('date')
            # total = Extract.objects.filter(user_name=user).aggregate(Sum('money'))

    elif request.method == 'GET':
        get_form = SelectExtractForm(request.GET)

        if get_form.is_valid():
            builds, total = Extract.objects.search_from_get(get_form)

    if not builds:
        builds = Extract.objects.filter(user_name=user).filter(date__gte=d).order_by('date')
        total = Extract.objects.filter(user_name=user).filter(date__gte=d).aggregate(Sum('money'))

    template_name = 'frameset_pages/line3.html'
    context = {
        'builds': builds,
        'total': total,
    }

    return render(request, template_name, context)


@login_required
def show_choice_data(request):
    get_form = SelectExtractForm()

    template_name = "frameset_pages/form2.html"
    context = {
        'get_form': get_form,
    }

    return render(request, template_name, context)


@login_required
def insert_data_form(request):
    form = EditExtractForm()

    template_name = "frameset_pages/form1.html"
    context = {
        'form': form,
    }

    return render(request, template_name, context)


def show_total(request):
    user = request.user

    payment_iterator = Extract.objects.filter(user_name=user).values_list(
        'payment').iterator()
    payment_list = set([i[0] for i in payment_iterator])

    total_account = [Extract.objects.filter(
        user_name=user, payment=conta).aggregate(Sum('money'))
                     for conta in payment_list]

    saldo = 0.0
    for resto in total_account:
        saldo += float(resto['money__sum'])

    template_name = 'frameset_pages/line1.html'
    context = {
        'payment_list': payment_list,
        'total_account': total_account,
        'saldo': saldo
    }
    return render(request, template_name, context)
