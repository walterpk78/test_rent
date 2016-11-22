# -*- coding: utf-8 -*-
import json
import logging
from .models import Transport
from django.http import HttpResponse


logger = logging.getLogger('api')


def ajax_response(**kwargs):
    # non cached reponse
    # needed for IE
    response = HttpResponse(**kwargs)
    response['Cache-Control'] = 'no-cache'
    return response


def list(request):
    j_dict = {}
    try:
        logger.info("Spin created dictionary: " + str(j_dict))
        return HttpResponse(content=json.dumps(j_dict), content_type='application/json')

    except Exception as e:
        logger.exception("Internal server error, Exception: " + str(e.message))
        return HttpResponse(content=json.dumps({}), content_type='application/json')



def ajax_list(request):
    agency_id = request.session['operator'].agency_id

    def convert_to_int(value):
        try:
            int_value = int(value)
        except (TypeError, ValueError):
            int_value = None
        return int_value

    filters = {
        'operation__customer__last_name__istartswith' : request.GET.get('customer_last_name', None),
        'operation__customer__first_name__istartswith': request.GET.get('customer_first_name', None),
        'operation__payer__last_name__istartswith'    : request.GET.get('payer_last_name', None),
        'operation__payer__first_name__istartswith'   : request.GET.get('payer_first_name', None),
        'operation__payment_mode'                     : request.GET.get('payment_mode', None),
        'operator_id'                                 : request.GET.get('operator_id', None),
        'status'                                      : request.GET.get('status', None),
        'id'                                          : convert_to_int(request.GET.get('id', None)),
        'ccp'                                         : convert_to_int(request.GET.get('ccp', None)),
        'reason'                                      : request.GET.get('reason', None),
        'executed_at_time_gte'                        : request.GET.get('executed_at_time_gte', None),
        'executed_at_time_lte'                        : request.GET.get('executed_at_time_lte', None),
        }
    filters = {filter_name:value for filter_name,value in filters.items() if value}

    try: page = int(request.GET.get('page'))
    except TypeError: page = 1

    try: pageSize = int(request.GET.get('pageSize'))
    except TypeError: pageSize = 10

    ob       = request.GET.get('orderBy', 'id')
    order_by = str(ob).split("|")

    if 'payer' in order_by: # order by payer ascending
        index = order_by.index('payer')
        order_by[index:index] = ['operation__payer__last_name', 'operation__payer__first_name']
    if '-payer' in order_by: # order by payer descending
        index = order_by.index('-payer')
        order_by[index:index] = ['-operation__payer__last_name', '-operation__payer__first_name']

    order_by_admitted = ['id', 'ccp', 'operation__payer__last_name', 'operation__payer__first_name', 'operation__amount_without_fee', 'operation__creation_time',]
    order_by_admitted = order_by_admitted + ['-'+ascendant_ord for ascendant_ord in order_by_admitted]
    order_by = [ord for ord in order_by if ord in order_by_admitted]

    from_row = (page-1)*pageSize if isinstance(page, int) and isinstance(pageSize, int) else 0
    to_row   = page*pageSize if isinstance(page, int) and isinstance(pageSize, int) else 0

    postal_slips = Transport.objects.list(agency_id=agency_id, filters=filters, order_by=order_by, from_row=from_row, to_row=to_row)

    return ajax_response(content_type='application/json', content=json.dumps({'postal_slips': postal_slips}))
    #return ajax_response(content_type='application/json', content=json.dumps({'postal_slips': [dict(ps.to_dict(), **{'scanner_image_url': ps.scanner_image_url}) for ps in postal_slips]}))
