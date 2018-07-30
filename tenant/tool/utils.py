# -*- coding: utf-8 -*-
import time

def dictfetchall(cursor):
    '''
    将返回结果转换成字典
    :param cursor:
    :return:
    '''

    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def is_valid_date(str):
  '''
  判断是否是一个有效的日期字符串
  '''

  try:
    time.strptime(str, "%Y-%m-%d")
    return True
  except:
    return False


def getDate(str=0):

    '''
    :return: 返回 '1970-01-01 00:00:01' 格式的时间
    '''
    if str == 0:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    else:
        return time.strptime(str, "%Y-%m-%d %H:%M:%S")


def arrayToJson(data):
    '''
    # 15hadoop-slave2 1.238MiB / 7.631GiB 0.02% 0.00% 810B / 0B, 0B / 0B
    :param data:
    :return:
    '''
    result = []
    for item in data:
        split = item.split('"')
        itemDict = {}
        for index in range(len(split)):
            if split[index] == ':':
                itemDict[split[index - 1]] = split[index + 1]
        result.append(itemDict)
    return result

