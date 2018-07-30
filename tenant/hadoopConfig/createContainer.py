import docker
from tenant.hadoopConfig.hostConfig import host

def createContainer(id, num,memory):
    '''
    base_url:  'tcp://192.168.103.211:2375'
    :param id:
    :param num:
    :return:
    '''
    url = 'tcp://%s:%s' % (host['ip'], host['port'])
    print(url)
    client = docker.DockerClient(base_url=url)
    print(client.version())
    print("打印版本信息")
    print(client.version()['Version'])
    print("列出当前存活的容器")
    container = client.containers.list()
    for i in container:
        print(i.name + '  ' + i.status + '  ')
    # 创建容器,分配网段
    client.containers.run(image='registry.cn-hangzhou.aliyuncs.com/zhouwentao/zwt:hadoop1.0',
                          name=str(id) + 'hadoop-master',
                          hostname=str(id) + 'hadoop-master',
                          network_mode='hadoop',mem_limit=memory,
                          detach=True, tty=True)

    # 针对节点个数，id创建新的容器
    node_count = num + 1
    for i in range(0, node_count - 1):
        print(i)
        client.containers.run(image='registry.cn-hangzhou.aliyuncs.com/zhouwentao/zwt:hadoop1.0',
                              name=str(id) + 'hadoop-slave' + str(i + 1),
                              hostname=str(id) + 'hadoop-slave' + str(i + 1),
                              network_mode='hadoop',mem_limit=memory,
                              detach=True, tty=True)
    print('创建集群成功')
    # dockernetwork = client.networks.list()
    # for i in dockernetwork:
    #     print(i.name)
    #     if(i.name == 'hadoop'):
    #         i.connect('zhou-slave')

