# -*- coding: utf-8 -*-
import json
import docker
from django.http import HttpResponse
from django.db import connection
from tenant.tool.utils import dictfetchall, getDate
from tenant.hadoopConfig.createContainer import createContainer
from tenant.hadoopConfig.reConfig import hadoopConfig
from tenant.hadoopConfig.replaceFiles import replaceFile
from tenant.hadoopConfig.hostConfig import host
import pandas as pd


def puyTenant(request):
    '''
    购买租户
    :param request:
    :return:
    '''
    label = request.GET.get('label')
    nodeCount = int(request.GET.get('nodeCount'))
    memory = request.GET.get('memory')
    update_at = getDate()
    create_at = getDate()
    users_id = request.COOKIES['phone']

    with connection.cursor() as cursor:
        sql = "insert into tenant(label,create_at,update_at,finish_at,users_id) " \
              "values('%s','%s','%s','%s','%s')" % (label, create_at, update_at, update_at, users_id)
        cursor.execute(sql)
        connection.commit()

        cursor.execute('select MAX(id) from tenant WHERE users_id=%s' % (users_id,))
        data = dictfetchall(cursor)
        sql = "insert into userstenant (tenant_id,users_id,permissions_id,creator,create_at,update_at)" \
              "values(%s,%s,%s,%s,'%s','%s')" \
              % (data[0]['MAX(id)'], users_id, 1, users_id, update_at, update_at)
        cursor.execute(sql)
        connection.commit()
    message = '购买成功'

    createContainer(int(data[0]['MAX(id)']), nodeCount,memory)
    hadoopConfig(int(data[0]['MAX(id)']), nodeCount)
    replaceFile(int(data[0]['MAX(id)']), nodeCount)
    return HttpResponse(message)


def ajaxToGetTenantInfo(request):
    name = request.COOKIES['phone']

    if name == 'null':
        return HttpResponse('error')
    else:

        with connection.cursor() as cursor:
            sql = "select * from tenant WHERE users_id=%s" % (name,)
            cursor.execute(sql)
            data = dictfetchall(cursor)

            for item in data:
                # item['id'] = '%dhadoop-master' % (item['id'],)
                item['create_at'] = str(item['create_at'])
                item['update_at'] = str(item['update_at'])
                item['finish_at'] = str(item['finish_at'])

            context = {'code': 0, 'msg': '请求数据', 'count': len(data), 'data': data}
            # print(type(context), context)
            return HttpResponse(json.dumps(context), content_type="application/json")


def ajaxToGetTenant(request):
    url = 'tcp://%s:%s' % (host['ip'], host['port'])
    print(url)
    client = docker.DockerClient(base_url=url)
    data = []
    id = request.GET.get('id')
    container = client.containers.list()
    for i in container:
        print(i.name)
        result = str.find(i.name, id)
        if (result == 0):
            temp={'name': i.name,'state': i.status}
            data.append(temp)
    print(data)
    context = {'code': 0, 'msg': '请求数据', 'count': len(data), 'data': data}
    return HttpResponse(json.dumps(context), content_type="application/json")


def ajaxToGetAllTenantStatus(request):
    name = request.COOKIES['phone']
    if name == 'null':
        return HttpResponse('error')
    else:
        id = request.GET.get('id')
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tenantstatus WHERE container LIKE '" + id + "%' ORDER BY create_at ASC"
            cursor.execute(sql)
            data = dictfetchall(cursor)
            data = pd.DataFrame(data)

            # columns = data.columns
            # Index(['BlockIO', 'container', 'cpu', 'create_at', 'id', 'networkIO',
            # 'percent', 'raw', 'update_at'],
            f_cpu = lambda x: float(x[:4])
            data['cpu'] = data['cpu'].map(f_cpu)
            data['percent'] = data['percent'].map(f_cpu)

            f_BlockIO = lambda x: x.split('/')
            data['BlockIO'] = data['BlockIO'].map(f_BlockIO)
            f_BlockIO = lambda x: x.split('/')
            data['networkIO'] = data['networkIO'].map(f_BlockIO)
            f_BlockIO = lambda x: x.split('/')
            data['raw'] = data['raw'].map(f_BlockIO)

            # 指定索引
            data1 = data.set_index('container').T.to_dict()
            data = data.set_index('id').T.to_dict()

            # 删除 id 的键值对，并把每个键的值转换为数组
            for item in data1:
                data1[item].pop('id')
                for index in data1[item]:
                    data1[item][index] = []
            for item in data:
                # 将timestamp 转换位 str
                data[item]['create_at'] = str(data[item]['create_at'])
                data[item]['update_at'] = str(data[item]['update_at'])

                for index in data1[data[item]['container']]:
                    data1[data[item]['container']][index].append(data[item][index])
            return HttpResponse(json.dumps(data1), content_type="application/json")


def ajaxToGetAddMember(request):

    name = request.COOKIES['phone']
    if name == 'null':
        return HttpResponse('error')
    else:
        phoneOrEmail = request.GET.get('phoneOrEmail')
        tenantId = request.GET.get('tenantId')
        with connection.cursor() as cursor:

            sql = "SELECT * FROM users WHERE phone='%s' OR email='%s'" % (phoneOrEmail, phoneOrEmail)
            if cursor.execute(sql) > 0:

                data = dictfetchall(cursor)
                sql = "SELECT * FROM userstenant WHERE tenant_id='%s' AND users_id='%s'" % (tenantId, data[0]['id'])
                if cursor.execute(sql) == 0:

                    sql = "INSERT INTO userstenant (tenant_id,users_id,permissions_id,creator,create_at,update_at) " \
                          "VALUES('%s','%s','%s','%s','%s','%s')" \
                          % (tenantId, data[0]['id'], 2, name, getDate(), getDate())
                    cursor.execute(sql)
                    connection.commit()
                    return HttpResponse('添加成功!')
                else:
                    return HttpResponse('用户已加入！')
            else:
                return HttpResponse('用户不存在！')

