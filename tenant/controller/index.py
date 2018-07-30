# -*- coding : utf-8 -*-
from django.db import connection
from django.shortcuts import render

from tenant.tool.utils import dictfetchall


def index(request):

    phone = request.COOKIES['phone']
    with connection.cursor() as cursor:
        sql = "select name from users WHERE phone=%s" % (phone)
        cursor.execute(sql)
        data = dictfetchall(cursor)
        print(data)
        name = {"name":data[0]['name']}
    if phone == 'null':
        return render(request, 'login.html')
    else:
        return render(request, 'index.html',name)


def welcome(request):
    name = request.COOKIES['phone']

    if name == 'null':
        return render(request, 'login.html')
    else:

        with connection.cursor() as cursor:
            sql = "select * from tenant WHERE users_id=%s" % (name,)
            cursor.execute(sql)
            data = dictfetchall(cursor)
            context = {"count": len(data)}
        return render(request, 'welcome.html', context)
