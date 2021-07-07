# -*- coding: utf-8 

import time
import os


# 获取上一次导入到 Anki 的时间
def getLastTimeOfToAnki():
    file = open('./上一次导入到Anki的时间', encoding='utf-8')
    lastTimeOfToAnki = file.read()
    file.close()

    lastTimeOfToAnki = float(lastTimeOfToAnki)

    return lastTimeOfToAnki


# 将这次导入到Anki的时间记录在文件中
def saveTheTimeOfToAnki(time):
    file = open('./上一次导入到Anki的时间', 'w', encoding='utf-8')
    file.write(str(time))
    file.close()


if __name__ == "__main__":

    a = getLastTimeOfToAnki()
    print(a)
    print(type(a))

    saveTheTimeOfToAnki(22)