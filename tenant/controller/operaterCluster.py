# -*- coding: utf-8 -*-
import json
import docker
from tenant.hadoopConfig.hostConfig import host
from django.http import HttpResponse
from django.db import connection
from tenant.tool.utils import dictfetchall, getDate
from tenant.hadoopConfig.createContainer import createContainer
from tenant.hadoopConfig.reConfig import hadoopConfig
from tenant.hadoopConfig.replaceFiles import replaceFile


# 添加节点
def addContainer(request):
    id = request.GET.get('id')
    id = int(id)
    print(id)
    url = 'tcp://%s:%s' % (host['ip'], host['port'])
    print(url)
    client = docker.DockerClient(base_url=url)
    with connection.cursor() as cursor:
        sql = "select label from tenant WHERE id=%d" % (int(id),)
        cursor.execute(sql)
        data = dictfetchall(cursor)
        print(data)
        # 新节点的个数
    newnodenumber = data[0]['label'] + 2
    if (newnodenumber >= 5):
        return HttpResponse('添加失败')
    # 修改tenant表中的label规格
    with connection.cursor() as cursor:
        sql = "update tenant set label='%d' WHERE id=%d" % (newnodenumber - 1, int(id))
        cursor.execute(sql)
        connection.commit()
    client.containers.run(image='kiwenlau/hadoop:1.0',
                          name=str(id) + 'hadoop-slave' + str(newnodenumber),
                          hostname=str(id) + 'hadoop-slave' + str(newnodenumber),
                          network_mode='hadoop',
                          detach=True, tty=True)
    hadoopConfig(int(id), newnodenumber)
    replaceFile(int(id), newnodenumber)
    return HttpResponse('添加成功')


# 删除节点

def deleteNode(request):
    deletenodename = request.GET.get('deletenodename')
    name = request.COOKIES['phone']
    print(deletenodename)
    result=str.find(deletenodename,'master')
    print("状态"+str(result))
    if name == 'null':
        return HttpResponse('error')
    if (result != -1):
        return HttpResponse("此节点为主节点，不可删除")
    id = request.GET.get('id')
    url = 'tcp://%s:%s' % (host['ip'], host['port'])
    print(url)
    client = docker.DockerClient(base_url=url)
    delete_master = client.containers.get(deletenodename)
    print(delete_master.name)
    # 关闭容器
    delete_master.stop()
    delete_master.remove()
    return HttpResponse("删除成功")
