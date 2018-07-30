from threading import Timer
from tenant.hadoopConfig.operateHadoop import seeContainerState
from tenant.tool.utils import getDate

import pymysql

# 打开数据库连接

def getContainerState():
    db = pymysql.connect(host='127.0.0.1', user='root', password='123', port=3306, db='Cloud',charset='utf8')
    cursor = db.cursor()
    result = seeContainerState()
    try:
        for item in result:

            # {'container': '16hadoop-slave1', 'raw': '1.223MiB / 7.631GiB',
            # 'percent': '0.02%', 'cpu': '0.00%', 'networkIO': '1.16kB / 0B,', 'BlockIO': '0B / 0B'}
            sql = "insert into tenantstatus (container, raw, percent, cpu, networkIO, BlockIO, update_at, create_at) " \
                  "values ('%s','%s','%s','%s','%s','%s','%s','%s')"\
                  % (item['container'], item['raw'], item['percent'], item['cpu'], item['networkIO'], item['BlockIO'], getDate(), getDate())
            print(sql)
            cursor.execute(sql)
            db.commit()
            print('successful')
    except Exception as e:
        print(e)
        db.rollback()

    # 关闭数据库连接
    db.close()


def fun_timer():
    getContainerState()
    global timer
    timer = Timer(5.5, fun_timer)
    timer.start()


timer = Timer(1, fun_timer)
timer.start()
