# -*- coding: utf-8 -*-
import json

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from tenant.tool.utils import dictfetchall


def tenant(request):
    name = request.COOKIES['phone']

    if name == 'null':
        return render(request, 'login.html')
    else:

        with connection.cursor() as cursor:
            sql = "select * from tenant WHERE users_id=%s" % (name,)
            cursor.execute(sql)
            data = dictfetchall(cursor)
            context = {"count": len(data)}
        return render(request, 'tenant/tenant.html', context)


def tenantManage(request):

    id = request.GET.get('id')
    return render(request, 'tenant/manage.html', context={"id": id})


def tenantUser(request):
    name = request.COOKIES['phone']

    if name == 'null':
        return render(request, 'login.html')
    else:
        return render(request, 'tenant/tenantuser.html')


def getTenantUser(request):
    name = request.COOKIES['phone']

    if name == 'null':
        return HttpResponse('err')
    else:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM userstenant WHERE tenant_id " \
                  "IN (SELECT id FROM tenant WHERE users_id = '%s') " \
                  "ORDER BY tenant_id;" \
                  % (name,)
            cursor.execute(sql)
            data = dictfetchall(cursor)
            print(data)
            for item in data:
                item['tenant_id'] = '%dhadoop-master' % (item['tenant_id'],)
                item['create_at'] = str(item['create_at'])
                item['update_at'] = str(item['update_at'])

            context = {'code': 0, 'msg': '请求数据', 'count': len(data), 'data': data}

        return HttpResponse(json.dumps(context))


def addTenant(request):
    name = request.COOKIES['phone']

    if name == 'null':
        return render(request, 'login.html')
    else:
        return render(request, 'tenant/addTenantList.html')


def getaddTenantList(request):
    name = request.COOKIES['phone']

    if name == 'null':
        return HttpResponse('err')
    else:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM userstenant WHERE creator != '%s' AND users_id = '%s'" % (name, name)
            cursor.execute(sql)
            data = dictfetchall(cursor)
            print(data)
            for item in data:
                item['tenant_id'] = '%dhadoop-master' % (item['tenant_id'],)
                item['create_at'] = str(item['create_at'])
                item['update_at'] = str(item['update_at'])

            context = {'code': 0, 'msg': '请求数据', 'count': len(data), 'data': data}

        return HttpResponse(json.dumps(context))


def monitorTenant(request):
    name = request.COOKIES['phone']

    if name == 'null':
        return render(request, 'login.html')
    else:
        id = request.GET.get('id')
        return render(request, 'tenant/monitorTenant.html', context={"id": id})
