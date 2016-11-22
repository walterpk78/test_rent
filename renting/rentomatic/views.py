import logging
import ast
from functools import wraps
from datetime import date, datetime
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http import QueryDict, HttpResponse, Http404
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import PaymentForm, RentForm
from .models import Transport, Rent
from .constants import MAX_CASH_AMOUNT

logger = logging.getLogger('api')


def render_to(template=None):
    def renderer(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            tmpl = output.pop('TEMPLATE', template)
            return render(request, tmpl, output)
        return wrapper
    return renderer


def make_change(amount, coins=(1, 2, 5, 10, 20, 50, 100, 200, 500), hand=None):
    hand = [] if hand is None else hand
    if amount == 0:
        yield hand
    for coin in coins:
        # ensures we don't give too much change, and combinations are unique
        if coin > amount or (len(hand) > 0 and hand[-1] < coin):
            continue
        for result in make_change(amount - coin, coins=coins, hand=hand + [coin]):
            yield result


def home(request):
    if request.method == 'GET':
        return render(request, "home.html", {})
    else:
        raise Http404


@render_to('help.html')
def help(request):
    return {}


@render_to('info.html')
def info(request):
    return {}


@render_to('list.html')
def list(request):
    # performance reference http://django-tables2.readthedocs.io/en/latest/pages/performance.html
    return {'transport': Transport.objects.all()}


def get_dict_from_request(request):
    post_dict = {
        "email": request.POST['id_email'],
        "end_date": datetime.strptime(request.POST['id_end_date'], "%Y-%m-%d"),
        "first_name": request.POST['id_first_name'],
        "last_name": request.POST['id_last_name'],
        "phone": request.POST['id_phone'],
        "start_date": datetime.strptime(request.POST['id_start_date'], "%Y-%m-%d"),
        "transport_id": request.POST['id_transport_id']
                }
    qdict = QueryDict('')
    qdict = qdict.copy()
    qdict.update(post_dict)
    return qdict


def get_form2_dict(request):
    new_dict = {
        "amount": int(round((float(str(request.POST['amount'])) * 100.0)))
    }
    qdict = QueryDict('')
    qdict = qdict.copy()
    qdict.update(new_dict)
    return qdict


@render_to('pay.html')
def pay(request, rent_dict={}):
    try:
        form = RentForm()
        form2 = PaymentForm()
        if len(rent_dict) != 0:
            transport = get_transport_obj(rent_dict['transport_id'])
            if transport is None:
                return render(request, 'payment_error.html', {"error": "Internal server error, please retry or call customer service"})
            total_amount = get_total(rent_dict['start_date'], rent_dict['end_date'], transport)
            rent_dict['start_date'] = str(rent_dict['start_date'])
            rent_dict['end_date'] = str(rent_dict['end_date'])
            return {"form2": form2, "rent_dict": rent_dict, "total_amount": round((total_amount / 100.0), 2)}
        elif request.method == 'POST':
            form2 = PaymentForm(get_form2_dict(request))
            cash_amount = int(round(float(str(request.POST['amount'])) * 100.0))
            try:
                if form2.is_valid():
                    form = RentForm(get_dict_from_request(request))
                    if not form.is_valid():
                        return {"form": form, "form2": form2}
                    logger.info("[@pay]Amount input: " + str(cash_amount))
                    transport = get_transport_obj(int(request.POST['id_transport_id']))
                    if transport is None:
                        return render(request, 'payment_error.html', {"error": "Internal server error, please retry or call customer service"})
                    logger.info("[@pay]Converted Amount input: " + str(cash_amount))
                    start_date = form.cleaned_data['start_date']
                    end_date = form.cleaned_data['end_date']
                    total_amount = get_total(start_date, end_date, transport)
                    if cash_amount < total_amount or cash_amount > MAX_CASH_AMOUNT:
                        form2._errors['amount'] = ErrorList([u"Amount is invalid or not allowed"])
                    else:
                        try:
                            rest = cash_amount - total_amount
                            change = 0
                            rest = round((rest / 100.0), 2)
                            cash_amount = round((cash_amount / 100.0), 2)
                            total_amount = round((total_amount / 100.0), 2)
                            if rest > 0:
                                for result in make_change(rest):
                                    change = result
                            try:
                                rent = Rent.objects.get(transport=transport, start_date=start_date, end_date=end_date)
                            except Exception as e:
                                rent = create_rent_record(transport, form.__dict__['cleaned_data'])
                            rent.rented = True
                            rent.save()
                            return render(request, 'pay_success.html', {"total_amount": total_amount, "cash_amount": cash_amount, "rest": rest, "change": change})
                        except Exception as e:
                            logger.exception("[@pay] Error in calculating rest and change, transport_id ")
                            return render(request, 'payment_error.html', {"error": "Internal server error, please retry or call customer service"})
            except Exception as e:
                logger.exception("[@pay] Internal exception while registering and creating db tables, Exception:" + str(e.message))
                return HttpResponse(mark_safe('<script>alert("Internal error, please retry or call customer service");window.location.href="'+reverse('home')+'";</script>'))
        if len(rent_dict) == 0:
            return {"form": form, "form2": form2}
        else:
            return {"rent_dict": rent_dict, "form2": form2}
    except Exception as e:
        logger.exception("[@pay] Internal error, Exception: " + str(e.message))
        return render(request, 'payment_error.html', {"error": "Internal server error, please retry or call customer service"})


def create_rent_record(transport, rent_dict):
    r = Rent.objects.filter(transport=transport, end_date__gte=rent_dict['start_date']).filter(~Q(rented=False)).filter(
        start_date__lte=rent_dict['end_date']).filter(Q(
        start_date__range=(rent_dict['start_date'], rent_dict['end_date'])) | Q(
        end_date__range=(rent_dict['start_date'], rent_dict['end_date'])))

    if len(r) == 0:
        try:
           r = Rent.objects.get(transport=transport, start_date=rent_dict['start_date'], end_date=rent_dict['end_date'],
                                rented=False)
        except:
            pass
        else:
            r.delete()
        rent = Rent.objects.create(
            first_name         = rent_dict['first_name'],
            last_name          = rent_dict['last_name'],
            email              = rent_dict['email'],
            phone              = rent_dict['phone'],
            transport          = transport,
            amount             = get_total(rent_dict['start_date'], rent_dict['end_date'], transport),
            start_date         = rent_dict['start_date'],
            end_date           = rent_dict['end_date'],
            rented             = False,
        )
        return rent
    else:
        raise Exception("[@create_rent_record] date interval already exist")

@render_to('rent.html')
def rent(request):
    if request.method == 'POST':
        form = RentForm(request.POST)
        try:
            if form.is_valid():
                rent_dict = form.__dict__['cleaned_data']
                t = get_transport_obj(request.POST['transport_id'])
                try:
                    rent = create_rent_record(t, rent_dict)
                except Exception as e:
                    logger.exception("[@pay] Unable to create rent record in DB , or already exits, Exception: " + str(e.message))
                    form._errors['start_date'] = ErrorList([u"Start Date is invalid or already rented"])
                    form._errors['end_date'] = ErrorList([u"End Date is invalid or already rented"])
                    return {'form': form}
                return pay(request, rent_dict)
        except Exception as e:
            logger.exception("[@rent] Exception: " + str(e.message))
            raise Http404
    elif request.method == 'GET':
        form = RentForm()
        return {'form': form}


def get_total(start_date, end_date, transport):
    delta = end_date - start_date
    total_amount = transport.price_per_day * delta.days
    return total_amount


def get_transport_obj(transport_id):
    try:
        transport = Transport.objects.get(id=transport_id)
    except Exception as e:
        logger.exception("[@pay] Error to get table Transport with id: " + str(transport_id))
        return None
    else:
        return transport


@render_to('update_km.html')
def update_km(request):
    pass