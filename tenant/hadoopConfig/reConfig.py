import os


def hadoopConfig(id, num):
    '''
    :param id:
    :param num:
    :return:
    '''
    print('hello')
    # 获取项目根目录 eg: G:\t\tenant
    path = os.getcwd()

    # 修改core-site.xml
    # 打开旧文件
    f = open('%s/static/hadoop-cluster-docker-master/config/core-site.xml' % (path,), 'r', encoding='utf-8')

    print(f)

    # 打开新文件
    f_new = open('%s/static/hadoop-cluster-docker-master/config/core-site11.xml' % (path,), 'w', encoding='utf-8')

    # 循环读取旧文件
    for line in f:
        # 进行判断
        if "<value>hdfs:" in line:
            line = line.replace(line, '        <value>hdfs://%dhadoop-master:9000/</value>\n' % id)
        f_new.write(line)

    f.close()
    f_new.close()
    os.remove('%s/static/hadoop-cluster-docker-master/config/core-site.xml' % (path,))
    os.rename('%s/static/hadoop-cluster-docker-master/config/core-site11.xml' % (path,),
              '%s/static/hadoop-cluster-docker-master/config/core-site.xml' % (path,))

    # 修改yarn-site.xml
    # 打开旧文件
    f = open('%s/static/hadoop-cluster-docker-master/config/yarn-site.xml' % (path,), 'r', encoding='utf-8')

    # 打开新文件
    f_new = open('%s/static/hadoop-cluster-docker-master/config/yarn-site11.xml' % (path,), 'w', encoding='utf-8')

    # 循环读取旧文件
    for line in f:
        # 进行判断
        if "hadoop-master</value>" in line:
            line = line.replace(line, '        <value>%dhadoop-master</value>\n' % id)
        f_new.write(line)

    f.close()
    f_new.close()
    os.remove('%s/static/hadoop-cluster-docker-master/config/yarn-site.xml' % (path,))
    os.rename('%s/static/hadoop-cluster-docker-master/config/yarn-site11.xml' % (path,),
              '%s/static/hadoop-cluster-docker-master/config/yarn-site.xml' % (path,))

    # slaves
    # 打开新文件
    f_new = open('%s/static/hadoop-cluster-docker-master/config/slaves11' % (path,), 'w', encoding='utf-8')

    # 循环读取旧文件
    for i in range(num):
        # data节点（id+hadoop-slave+编号）
        f_new.write('%dhadoop-slave%d\n' % (id, i + 1))

    f_new.close()
    os.remove('%s/static/hadoop-cluster-docker-master/config/slaves' % (path,))
    os.rename('%s/static/hadoop-cluster-docker-master/config/slaves11' % (path,),
              '%s/static/hadoop-cluster-docker-master/config/slaves' % (path,))

    # 修改ssh_config
    # 打开旧文件
    f = open('%s/static/hadoop-cluster-docker-master/config/ssh_config' % (path,), 'r', encoding='utf-8')

    # 打开新文件
    f_new = open('%s/static/hadoop-cluster-docker-master/config/ssh_config11' % (path,), 'w', encoding='utf-8')

    # 循环读取旧文件
    for line in f:
        # 进行判断
        if "hadoop-*" in line:
            line = line.replace(line, 'Host %dhadoop-*\n' % id)
        f_new.write(line)

    f.close()
    f_new.close()
    os.remove('%s/static/hadoop-cluster-docker-master/config/ssh_config' % (path,))
    os.rename('%s/static/hadoop-cluster-docker-master/config/ssh_config11' % (path,),
              '%s/static/hadoop-cluster-docker-master/config/ssh_config' % (path,))
