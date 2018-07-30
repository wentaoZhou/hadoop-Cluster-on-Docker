import os
import paramiko
from tenant.hadoopConfig.hostConfig import host

def replaceFile(id, num):
    '''

    :param id:
    :param num:
    :return:
    '''
    # 获取项目根目录 eg: G:\t\tenant
    path = os.getcwd()

    transport = paramiko.Transport(host['ip'], 22)
    transport.connect(username=host['name'], password=host['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('%s/static/hadoop-cluster-docker-master/config/core-site.xml' % (path,), '/opt/hadoop/core-site.xml')
    sftp.put('%s/static/hadoop-cluster-docker-master/config/yarn-site.xml' % (path,), '/opt/hadoop/yarn-site.xml')
    sftp.put('%s/static/hadoop-cluster-docker-master/config/slaves' % (path,), '/opt/hadoop/slaves')
    sftp.put('%s/static/hadoop-cluster-docker-master/config/ssh_config' % (path,), '/opt/.ssh/config')
    transport.close()


    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host['ip'], 22, host['name'], host['password'])
    for i in range(num+1):
        if(i == 0):
            stdin, stdout, stderr = ssh.exec_command("docker cp /opt/hadoop %dhadoop-master:/usr/local/hadoop/etc/" % id)
            stdin, stdout, stderr = ssh.exec_command("docker cp /opt/.ssh %dhadoop-master:/root" % id)
        else:
            stdin, stdout, stderr = ssh.exec_command("docker cp /opt/hadoop %dhadoop-slave%d:/usr/local/hadoop/etc/"
                                                     % (id, i))
            stdin, stdout, stderr = ssh.exec_command("docker cp /opt/.ssh %dhadoop-slave%d:/root" % (id, i))

    ssh.close()
