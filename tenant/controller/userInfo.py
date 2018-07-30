# -*- coding:utf8 -*-
from django.db import connection
from django.shortcuts import render
from tenant.tool.utils import dictfetchall


def userinfo(request):
    name = request.COOKIES['phone']
    if name == 'null':
        return render(request, 'login.html')
    else:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE phone = '%s'"\
                  % (name,)
            cursor.execute(sql)
            data = dictfetchall(cursor)
            for item in data:
                item['create_at'] = str(item['create_at'])
                item['update_at'] = str(item['update_at'])
            print(data)
        return render(request, 'userInfo.html', context=data[0])
