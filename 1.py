# -*- coding:utf-8 -*-
# 运行环境 Python3 , 将代码放在需要修改的快捷方式路径下执行
import os
import time
from itertools import permutations
import progressbar  # 自行安装此Module

#
# C:\Users\Administrator\Desktop> D:/Python36/python.exe 1.py
# *注意事项*
# 如果发现执行完成后，有部分快捷方式没有修改，请查看这些快捷方式是否在其他路径下。
# 有个人用户桌面和公用桌面等路径的存在
#

# arr=[u'\u2061',u'\u2062',u'\u2063',u'\u2064',u'\u206A',u'\u206B',u'\u206C',u'\u206D',u'\u206E',u'\u206F',u'\u202A',u'\u202B',u'\u202C',u'\u202D',u'\u202E',u'\u202F',u'\u200B',u'\u200C',u'\u200D',u'\u200E',u'\u200F']
arr = [u'\u2061', u'\u2062', u'\u2063', u'\u2064',
       u'\u206A', u'\u206B', u'\u206C', u'\u206D']
lnks = []
lnkNames = []
p = progressbar.ProgressBar()


def getlnks():
    files = os.listdir('.')
    for file in files:
        filename, type = os.path.splitext(file)
        if type != '.lnk':
            continue
        lnks.append(file)
        lnkNames.append(filename.encode('utf-8'))


def change():
    names = []
    for t in list(permutations(arr)):
        strs = b''
        for s in t:
            strs += s.encode('utf-8')
        names.append(strs)
    p.maxval = len(lnks)
    for lnk in lnkNames:
        try:
            names.index(lnk)
            names.remove(lnk)
        except ValueError:
            continue
    p.start()
    for i, file in enumerate(lnks):
        p.update(i+1)
        time.sleep(0.1)
        for items in names:
            if items in lnkNames:
                names.remove(items)
                continue
            else:
                names.remove(items)
                lnkNames.append(items)
                os.rename(file, items.decode('utf-8')+'.lnk')
                break


def clear():
    print('清空快捷方式图标', os.system(
        r'reg delete "HKEY_CLASSES_ROOT\lnkfile" /v IsShortCut /f'))
    time.sleep(1)
    print('重启资源管理器', os.system(r'taskkill /f /im explorer.exe'))
    time.sleep(2)
    print(os.system('start explorer.exe'))


if __name__ == '__main__':
    getlnks()
    change()
    p.finish()
    clear()
