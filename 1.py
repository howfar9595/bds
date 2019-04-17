# 运行环境 Python3
from __future__ import print_function
import os
import time
from itertools import permutations
import progressbar  # 自行安装此Module
import ctypes

#
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

path = os.path.expanduser('~/Desktop/')


def getlnks():
    paths = [os.path.expanduser('~/Desktop/'), 'C:/Users/Public/Desktop/']
    for path in paths:
        for file in os.listdir(path):
            filename, type = os.path.splitext(file)
            if type != '.lnk':
                continue
            lnks.append((path, file))
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
    for i, fileTuple in enumerate(lnks):

        p.update(i+1)
        time.sleep(0.1)
        for items in names:
            if items in lnkNames:
                names.remove(items)
                continue
            else:
                names.remove(items)
                lnkNames.append(items)
                os.rename(fileTuple[0] + fileTuple[1],
                          fileTuple[0] + items.decode('utf-8')+'.lnk')
                break


def clear():
    print('Clear shortcut small arrow.', os.system(
        r'reg delete "HKEY_CLASSES_ROOT\lnkfile" /v IsShortCut /f'))
    time.sleep(1)
    print('Restart the resource manager.',
          os.system(r'taskkill /f /im explorer.exe'))
    time.sleep(2)
    print(os.system('start explorer.exe'))


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    if is_admin():
        getlnks()
        change()
        p.finish()
        clear()
    else:
        print('Please run cmd in admin mode.')
