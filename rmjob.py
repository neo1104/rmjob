# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os
import re
import time


# 读取文件内容
def ProcessConfigure(con_file):
    fs = open(conf_file)
    jobs = list()
    for line in fs.readlines(256):
        if line.startswith('#'):     #跳过注释行
            continue
        line = line.strip('\t\r\n')
        l = line.split()
        #填充job信息
        job = dict()
        job['path'] = l[0]
        job['pattern'] = l[1]
        # 解析时间跨度
        if not re.match(r'[1-9]+[Dd|Hh|Mm|Ss]$', l[2]):
            print('[%s] confiure error' % job['path'])
            exit()
        t = l[2][-1]
        if t == 'd' or t == 'D':
            job['time'] = int(l[2][0:-1]) * 24 * 60 * 60    #日
        elif t == 'h' or t == 'H':
            job['time'] = int(l[2][0:-1]) * 60 * 60         #小时
        elif t == 'M' or t == 'm':
            job['time'] = int(l[2][0:-1]) * 60              #分钟
        else:
            job['time'] = int(l[2][0:-1])                   #秒
        jobs.append(job)
    fs.close()
    print(jobs)
    return jobs

# 开始处理job
def Run(jobs):
    for job in jobs:
        if not os.path.isdir(job['path']):
            continue   #跳过不存在的路径
        prog = re.compile(job['pattern'])
        # 读取指定路径内的指定的文件名，并判断修改时间，如果修改时间符合，则进行删除操作
        files = os.listdir(job['path'])
        for file in files:
            if not prog.match(file):
                continue
            # 如果文件模式匹配，则获取对应文件的修改时间
            f = os.path.join(job['path'], file)
            # 跳过目录
            if os.path.isdir(f):
                continue
            if not os.path.isfile(f):
                continue
            mtime = os.path.getmtime(f)
            # 判断文件的最后一次修改时间是否已经超出指定时间
            if time.time() - mtime >= job['time']:
                os.remove(f)
    print('Jobs Run Done.')

if __name__ == '__main__':
    # 判断脚本命令使用方式是否正确
    if len(sys.argv) != 2:
        print('use: rmjob <rm job configure file>')
        exit()
    conf_file = sys.argv[1]

    # 判断指定的配置文件是否存在
    if not os.path.isfile(conf_file):
        print('%s not exist' % conf_file)
        exit()
    jobs = ProcessConfigure(conf_file)
    Run(jobs)
