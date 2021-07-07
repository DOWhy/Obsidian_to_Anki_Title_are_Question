# -*- coding: utf-8 

import re
import os
from shutil import copyfile # 复制文件用的


# 将 [[...]] 链接变成蓝色
def turnInlineLinkToRed(bookToTxt):
    file1 = open(bookToTxt, encoding="utf-8")
    context = file1.readlines()
    file1.close()

    i = 0
    for i in range(len(context)):
        print('将 [[...]] 链接变成蓝色：' + str(i))
        if re.match(r'\[\[.*?\]\]', context[i]):
            str2 = re.match(r'(\[\[.*?\]\])', context[i]).group(1)
            context[i] = context[i].replace(str2, '<font color="blue"><u>' + str2 + '</u></font>')
        if re.search(r'[^!]\[\[.*?\]\]', context[i]):
            teststr = re.findall(r'[^!]\[\[.*?\]\]', context[i])
            for test_str in teststr:
                a = test_str[0]
                context[i] = context[i].replace(test_str, a + '<font color="blue"><u>' + test_str[1:] + '</u></font>')

    file4 = open(bookToTxt, 'w', encoding="utf-8")
    file4.writelines(context)
    file4.close()


# 将文件中的 ~~ 变成 <del></del>
def turnDeleteLine(bookToTxt):
    file1 = open(bookToTxt, encoding="utf-8")
    context = file1.readlines()
    file1.close()

    i = 0
    for i in range(len(context)):
        print('将文件中的 ~~ 变成 <del></del>：' + str(i))

        # 看看这一行里有没有 ~~
            # 如果没有，继续处理下一行
            # 如果有，需要转换

        if '~~' not in context[i]:
            continue
        else:
            while '~~' in context[i]:
                    context[i] = context[i].replace('~~', '<del>', 1)  # 因为 ~~ 是成对出现，所以这里替换第一个 ~~
                    context[i] = context[i].replace('~~', '</del>', 1) # 替换第二个 ~~

    file4 = open(bookToTxt, 'w', encoding="utf-8")
    file4.writelines(context)
    file4.close()


# 转换行内 latex
def turnInlineLatex(bookToTxt):
    file1 = open(bookToTxt, encoding="utf-8")
    context = file1.readlines()
    file1.close()

    i = 0
    for i in range(len(context)):
        print('转换行内 latex：' + str(i))
        # 看看这一行里有没有 $
            # 如果没有，继续处理下一行
            # 如果有，需要遍历这一行的每个字符
                # 看看 $ 前面有没有 \
                    # 如果这一行的第一个字符就是 $，它前面肯定没有 \
                    # 如果没有，则说明这个 $ 是 latex 符号，如果有，说明这是一个普通的 $ 

        if '$' not in context[i]:
            continue
        else:
            k1 = 0
            k2 = 0
            j = 0

            for j in range(len(context[i])):
                if j == 0:
                    if context[i][j] == '$':
                        k1 = j+1  # j+1 是为了让 k1 不等于0，后面用 k1 的时候还需要减去 1
                else:
                    if context[i][j] == '$':
                        if context[i][j-1] == '\\':
                            continue
                        else:
                            if k1 != 0:
                                k2 = j
                            else:
                                k1 = j+1
                
                if k1 != 0 and k2 != 0:
                    context[i] = context[i][:k1-1] + '\(' + context[i][k1:k2] + '\)' + context[i][k2+1:]
                    k1 = 0
                    k2 = 0

                            


        # # 在 obsidian 中 $ 起latex作用，要输入纯 $,需要使用 \$
        # # 在正则表达式中要匹配 \ 需要使用 \\,因为 \ 本身有转义的意思
        # if re.match(r'\$.*?[^\\]\$', context[i]): #如果latex出现在行尾，那么最后可能没有空格
        #     li = re.match(r'(\$[^ ].*?[^\\]\$)', context[i]).group(1)
        #     test = li
        #     li = r"\(" + li[1:-1] + r'\)'
        #     context[i] = context[i].replace(test, li)
        # if re.search(r'[^\\]\$[^ ].*?[^\\]\$', context[i]): #如果latex出现在行尾，那么最后可能没有空格
        #     list1 = re.findall(r'[^\\]\$[^ ].*?[^\\]\$', context[i])
        #     for li in list1:
        #         test = li
        #         if li[0] != " ":
        #             li = li[0] + r" \(" + li[2:-1] + r'\)'
        #         else:
        #             li = r" \(" + li[2:-1] + r'\)'
        #         # str1 = re.search(r'([^\]\$)[^ ].*?[^ ]\$', context[i]).group(1)
        #         # str2 = re.search(r'[^\]\$[^ ].*?[^ ](\$)', context[i]).group(1)
        #         # li = li.replace(str1, ' \(')
        #         # li = li.replace(str2, '\)')
        #         context[i] = context[i].replace(test, li)

    file4 = open(bookToTxt, 'w', encoding="utf-8")
    file4.writelines(context)
    file4.close()


# 获取 Anki 媒体文件夹内的所有文件名
def _getAnkiCollectionMediaFiles():
    path = 'C:\\Users\\john\\AppData\\Roaming\\Anki2\\账户1\\collection.media'
    ankiMediaFiles = os.listdir(path)
    return ankiMediaFiles


# 将图片、视频等复制到 anki 的媒体文件夹
def copyMediaToAnki(bookToTxt):
    file1 = open(bookToTxt, encoding="utf-8")
    context = file1.readlines()
    file1.close()

    ankiMediaFiles = _getAnkiCollectionMediaFiles()
    sdir = 'c:\\Users\\john\\Documents\\zettelkasten2\\zltr\\'
    ddir = 'C:\\Users\\john\\AppData\\Roaming\\Anki2\\账户1\\collection.media\\'

    i = 0
    for i in range(len(context)):
        if re.search(r'!\[\[.*?\]\]', context[i]):
            files = re.findall(r'!\[\[.*?\]\]', context[i])
            for file in files:
                test = file[3:-2]
                if test.endswith('mp4') or test.endswith('mpeg') or test.endswith('mp3') or test.endswith('flv') or test.endswith('mkv'):
                    if test not in ankiMediaFiles:
                        copyfile(sdir + test, ddir + test) # 复制文件
                        print('复制媒体文件：' + str(i) + '    ' + test)        
                    context[i] = context[i].replace(file, '[sound:' + test + ']')
                elif test.endswith('jpg') or test.endswith('jpeg') or test.endswith('png') or test.endswith('svg') or test.endswith('gif') or test.endswith('bmp'):
                    if test not in ankiMediaFiles:
                        copyfile(sdir + test, ddir + test) # 复制文件
                        print('复制媒体文件：' + str(i) + '    ' + test)
                    context[i] = context[i].replace(file, '<img src="' + test + '">')
        # elif re.search(r'!\[.*?\]\(.*?\)', context[i]):
        #     files = re.findall(r'!\[.*?\]\(.*?\)', context[i])
        #     for file in files:
        #         test = re.search(r'!\[.*?\]\((.*?)\)', file).group(1)
        #         if test.endswith('mp4') or test.endswith('mpeg') or test.endswith('mp3') or test.endswith('flv') or test.endswith('mkv'):
        #             # copyfile(sdir + test[4:], ddir + test[4:]) # 复制文件
        #             context[i] = context[i].replace(file, '[sound:' + test + ']')
        #         elif test.endswith('jpg') or test.endswith('jpeg') or test.endswith('png') or test.endswith('svg') or test.endswith('gif') or test.endswith('bmp'):
        #             # copyfile(sdir + test[4:], ddir + test[4:]) # 复制文件
        #             context[i] = context[i].replace(file, '<img src="' + test + '">')

    file4 = open(bookToTxt, 'w', encoding="utf-8")
    file4.writelines(context)
    file4.close()


if __name__ == "__main__":
    print('hello')

    bookToTxt = 'C:\\Users\\john\\Downloads\\question.txt'
    copyMediaToAnki(bookToTxt)

    _getAnkiCollectionMediaFiles()