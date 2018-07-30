# -*- coding: utf-8 -*-
import paramiko
import json
import docker
from tenant.hadoopConfig.hostConfig import host
from django.http import HttpResponse
from django.db import connection
from tenant.tool.utils import dictfetchall, getDate
from tenant.hadoopConfig.createContainer import createContainer
from tenant.hadoopConfig.reConfig import hadoopConfig
from tenant.hadoopConfig.replaceFiles import replaceFile
from tenant.hadoopConfig.hostConfig import host
from tenant.tool.utils import arrayToJson


def startHadoop(request):
    '''
    :param id:    id=int

    :return:
    '''
    id = request.GET.get('id')
    id=int(id)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接主机
    ssh.connect(host['ip'], 22, host['name'], host['password'])
    stdin, stdout, stderr = ssh.exec_command("docker exec -i %dhadoop-master bash start-hadoop.sh" % id)
    print(stdout.readlines())
    ssh.close()
    # 修改租户的状态
    with connection.cursor() as cursor:
        sql = "update tenant set status='Running' WHERE id=%d" % (int(id))
        cursor.execute(sql)
        connection.commit()
    return HttpResponse("开启成功")

def stopHadoop(request):
    '''
    :param id:
    :return:
    '''
    id = request.GET.get('id')
    id = int(id)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接主机
    ssh.connect(host['ip'], 22, host['name'], host['password'])
    stdin, stdout, stderr = ssh.exec_command("docker exec -i %dhadoop-master bash /usr/local/hadoop/sbin/stop-all.sh" % id)
    print(stdout.readlines())
    ssh.close()
    # 修改租户的状态
    with connection.cursor() as cursor:
        sql = "update tenant set status='notRunning' WHERE id=%d" % (int(id))
        cursor.execute(sql)
        connection.commit()
    return HttpResponse("关闭成功")


def seeContainerState():
    '''
    查看容器状态
    :return:
    '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host['ip'], 22, host['name'], host['password'])
    stdin, stdout, stderr = ssh.exec_command(
        "docker stats --no-stream --format     '{\"container\":\"{{ .Name }}\",\"memory\":{\"raw\":\"{{ .MemUsage }}\",\"percent\":\"{{ .MemPerc }}\"},\"cpu\":\"{{ .CPUPerc }}\",\"networkIO\":\"{{.NetIO}},\"BlockIO\":\"{{.BlockIO}}\"}'")
    result = stdout.readlines()

    return arrayToJson(result)
