# -*- coding: utf-8 -*-
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from tenant.tool.utils import getDate, dictfetchall


def login(request):
    return render(request, 'login.html')

@csrf_exempt
def loginForm(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            sql = "select * from  users where phone=%s" % (phone,)
            low = cursor.execute(sql)

            if low == 1:
                result = dictfetchall(cursor)
                if result[0]['password'] == password:
                    data = "登录成功"
                    response = HttpResponse(data)
                    response.set_cookie('phone', phone)
                else:
                    data = "密码错误"
                    response = HttpResponse(data)
            else:
                data = "用户不存在！"
                response = HttpResponse(data)
            connection.commit()
    return response


def register(request):

    return render(request, 'register.html')


@csrf_exempt
def registerForm(request):
    '''
    注册表单提交
    :param request:
    :return:
    '''

    name = request.POST.get('name')
    password = request.POST.get('password')
    email = request.POST.get('email')
    phone = request.POST.get('phone')

    update_at = getDate()
    create_at = getDate()

    with connection.cursor() as cursor:
        sql = "insert into users(name,phone,email,password,update_at,create_at) " \
               "VALUES('%s','%s','%s','%s','%s','%s')" \
               % (name, phone, email, password, update_at, create_at)
        cursor.execute(sql)
        connection.commit()

    return HttpResponse("注册成功")