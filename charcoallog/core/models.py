from django.shortcuts import redirect
from django.contrib import messages
from django.db import models
from django.db.models import Sum
from django.db import IntegrityError, transaction
from django.core.urlresolvers import reverse


# from django.utils import timezone
# import Q ?

class ExtractManager(models.Manager):
    def search_from_get(self, request_get, form):
        # user_name = form.cleaned_data.get('user_name')
        user_name = request_get.user
        columm = form.cleaned_data.get('columm')
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')
        value = {(columm,)}

        if columm.lower() == 'all':
            bills = self.filter(user_name=user_name).filter(
                date__gte=from_date, date__lte=to_date).order_by('-date')

            total = self.filter(user_name=user_name).filter(
                date__gte=from_date, date__lte=to_date).aggregate(Sum('money'))

            return bills, total

        # elif value.issubset(set(self.filter(user_name=user_name).values_list('payment'))):
        elif self.filter(user_name=user_name, payment__contains=columm):
            bills = self.filter(user_name=user_name, payment=columm).filter(
                date__gte=from_date, date__lte=to_date).order_by('-date')

            total = self.filter(user_name=user_name, payment=columm).filter(
                date__gte=from_date, date__lte=to_date).aggregate(Sum('money'))

            return bills, total

        # elif value.issubset(set(self.filter(user_name=user_name).values_list('category'))):
        elif self.filter(user_name=user_name, category__contains=columm):
            bills = self.filter(user_name=user_name, category=columm).filter(
                date__gte=from_date, date__lte=to_date).order_by('-date')

            total = self.filter(user_name=user_name, category=columm).filter(
                date__gte=from_date, date__lte=to_date).aggregate(Sum('money'))

            return bills, total

        # elif value.issubset(set(self.filter(user_name=user_name).values_list('description'))):
        elif self.filter(user_name=user_name, description__contains=columm):
            bills = self.filter(user_name=user_name, description=columm).filter(
                date__gte=from_date, date__lte=to_date).order_by('-date')

            total = self.filter(user_name=user_name, description=columm).filter(
                date__gte=from_date, date__lte=to_date).aggregate(Sum('money'))

            return bills, total

        else:
            messages.error(request_get, "Invalid search!")
            return redirect('core:show_data'), 0

    def insert_by_post(self, form):
        # user_name = form.cleaned_data.get('user_name')
        # date = form.cleaned_data.get('date')
        # money = form.cleaned_data.get('money')
        # description = form.cleaned_data.get('description')
        # category = form.cleaned_data.get('category')
        # payment = form.cleaned_data.get('payment')
        # remove = form.cleaned_data.get('remove')

        try:
            with transaction.atomic():
                if form.cleaned_data.get('remove'):
                    user_name = form.cleaned_data.get('user_name')
                    date = form.cleaned_data.get('date')
                    money = form.cleaned_data.get('money')
                    description = form.cleaned_data.get('description')
                    category = form.cleaned_data.get('category')
                    payment = form.cleaned_data.get('payment')

                    self.filter(user_name=user_name, date=date, money=money,
                                description=description, category=category,
                                payment=payment).order_by('id')[0].delete()
                else:
                    form.save()
                    # self.create(user_name=user_name, date=date, money=money,
                    #            description=description, category=category,
                    #            payment=payment)
                    # notify user is ok ? messages()
        except IntegrityError:
            # messages()
            print("An error happened")
            return redirect(reverse('Extract-settings'))
        except IndexError:
            print("Do not Refresh the page!!!")

    def delete(self, query):
        return self.filter(query).delete()


class Extract(models.Model):
    user_name = models.CharField('Name', max_length=30)
    date = models.DateField('Date')
    money = models.FloatField('Money', default=00.00, null=False, blank=False)
    description = models.CharField('Description', max_length=70)
    category = models.CharField('Category', max_length=70)
    payment = models.CharField('Payment', max_length=70)

    objects = ExtractManager()

    class Meta:
        ordering = ['-date']
