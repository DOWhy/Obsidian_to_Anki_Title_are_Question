# -*- coding: utf-8 

import markdown
import os
import sys
import re
from shutil import copyfile # 复制文件用的
import uuid


# 将图片、视频等复制到 anki 的媒体文件夹
def copyMediaToAnki(bookToTxt):
    file1 = open(bookToTxt, encoding="utf-8")
    context = file1.readlines()
    file1.close()

    i = 0
    for i in range(len(context)):
        print('复制媒体文件：' + str(i))
        if re.search(r'!\[\[.*?\]\]', context[i]):
            files = re.findall(r'!\[\[.*?\]\]', context[i])
            for file in files:
                test = file[3:-2]
                if test.endswith('mp4') or test.endswith('mpeg') or test.endswith('mp3') or test.endswith('flv') or test.endswith('mkv'):
                    # copyfile(sdir + test, ddir + test) # 复制文件
                    context[i] = context[i].replace(file, '[sound:' + test + ']')
                elif test.endswith('jpg') or test.endswith('jpeg') or test.endswith('png') or test.endswith('svg') or test.endswith('gif') or test.endswith('bmp'):
                    # copyfile(sdir + test, ddir + test) # 复制文件
                    context[i] = context[i].replace(file, '<img src="' + test + '">')
        elif re.search(r'!\[.*?\]\(.*?\)', context[i]):
            files = re.findall(r'!\[.*?\]\(.*?\)', context[i])
            for file in files:
                test = re.search(r'!\[.*?\]\((.*?)\)', file).group(1)
                if test.endswith('mp4') or test.endswith('mpeg') or test.endswith('mp3') or test.endswith('flv') or test.endswith('mkv'):
                    # copyfile(sdir + test[4:], ddir + test[4:]) # 复制文件
                    context[i] = context[i].replace(file, '[sound:' + test + ']')
                elif test.endswith('jpg') or test.endswith('jpeg') or test.endswith('png') or test.endswith('svg') or test.endswith('gif') or test.endswith('bmp'):
                    # copyfile(sdir + test[4:], ddir + test[4:]) # 复制文件
                    context[i] = context[i].replace(file, '<img src="' + test + '">')

    file4 = open(bookToTxt, 'w', encoding="utf-8")
    file4.writelines(context)
    file4.close()


# 转换超链接
def turnHyperLink(bookToTxt):
    file1 = open(bookToTxt, encoding="utf-8")
    context = file1.readlines()
    file1.close()

    i = 0
    for i in range(len(context)):
        print('转换超链接：' + str(i))
        if re.match(r'\[.*?\]\(.*?\)', context[i]):
            str2 = re.match(r'(\[.*?\]\(.*?\))', context[i]).group(1)
            str1 = re.search(r'\[(.*?)\]\(.*?\)', str2).group(1)
            str3 = re.search(r'\[.*?\]\((.*?)\)', str2).group(1)
            context[i] = context[i].replace(str2, '<a href="' + str3 + '">' + str1 + '</a>')
        if re.search(r'[^!]\[.*?\]\(.*?\)', context[i]):
            teststr = re.findall(r'[^!]\[.*?\]\(.*?\)', context[i])
            for test_str in teststr:
                a = test_str[0]
                str1 = re.search(r'[^!]\[(.*?)\]\(.*?\)', test_str).group(1)
                str3 = re.search(r'[^!]\[.*?\]\((.*?)\)', test_str).group(1)
                context[i] = context[i].replace(test_str, a + '<a href="' + str3 + '">' + str1 + '</a>')

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


# 转换块 latex
def turnBlockLatex(bookToTxt):
    file1 = open(bookToTxt, encoding="utf-8")
    context = file1.readlines()
    file1.close()

    line = 9999999999999999999999999999999999999 # 标注第多少行
    k = 1 # 标记是第几个 $$
    i = 0
    for i in range(len(context)):
        print('转换块 latex：' + str(i))
        if context[i].startswith('$$') and k == 1:
            line = i
            k = 2
            context[i] = context[i].rstrip() # 去掉行尾的空格,同时会去掉@%
            context[i] = r"\["
        elif i > line and not context[i].startswith('$$'):
            # context[i] = context[i].rstrip() # 去掉行尾的空格,同时会去掉@%
            context[i] = re.sub(r'@%', ' ', context[i])
        elif context[i].startswith('$$') and k == 2:
            k = 1
            line = 9999999999999999999999999999999999999
            context[i] = context[i].rstrip() # 去掉行尾的空格,同时会去掉@%
            context[i] = r'\]@%'

    file4 = open(bookToTxt, 'w', encoding="utf-8")
    file4.writelines(context)
    file4.close()

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

# 验证这一行是否是以 ^abo349 的格式结尾，如果不是给加上
def check_block_id(j, conlist, anki_cloze_list):
	if conlist[i].rstrip()[-7] == '^' and conlist[i].rstrip()[-8] == ' ':
		anki_cloze_list.append(conlist[i].rstrip()[-6:] + '@%' + conlist[i])
	else:
		j = 1
		id = uuid.uuid4()
		id = str(id)[-6:]
		if conlist[i].endswith('\n'):
			conlist[i] = conlist[i][:-1] + ' ^' + id + '\n'
		else:
			conlist[i] = conlist[i] + ' ^' + id + '\n'
		anki_cloze_list.append(conlist[i].rstrip()[-6:] + '@%' + conlist[i])
	return j



# 将 markdown 转换为 HTML，并且写入到 某个 文件中
def markdown2htmlAndWrite2question(anki, path): # 参数是数组

    content1 = "".join(anki) # 将列表变成一个字符串
    content1 = content1.replace('@%```', '@%\n```')
    content1 = content1.replace('<br>```', '<br>\n```')

    # file7 = open("C:\\Users\\john\\Downloads\\bbbba.txt", 'w', encoding='utf-8')
    # file7.write(content1)
    # file7.close()


    # extensions 参考： https://python-markdown.github.io/extensions/
    html = markdown.markdown(content1, extensions=['fenced_code', 'codehilite', 'tables', 'nl2br', 'extra', 'abbr', 'def_list', 'footnotes', 'md_in_html', 'admonition', 'legacy_attrs', 'legacy_em', 'meta', 'sane_lists', 'smarty', 'toc',  'pymdownx.highlight', 'pymdownx.inlinehilite', 'pymdownx.tasklist', 'pymdownx.caret', 'sane_lists', 'mdx_truly_sane_lists']) # 'wikilinks', 这个是将 [[]] 转换为内部链接的。  'pymdownx.arithmatex', markdown 中的 latex 转换为 HTML

    # file6 = open("C:\\Users\\john\\Downloads\\aaaab.txt", 'w', encoding='utf-8')
    # file6.write(html)
    # file6.close()

    # 转换文件中的标签。虽然文件中标签的格式是：“#xxx”，但是python依然会将它识别为一级标题，转换成“<h1>”标签的形式，所以这里将<h1>标签进行转换
    taglist = re.findall(r'<h1.*>.*</h1>', html)
    if taglist != []:
        j = 0
        for j in range(len(taglist)):
            if re.search(r'<h1.*>(.*)</h1>', html):
                tag = re.search(r'<h1.*>(.*)</h1>', html).group(1)
                html = re.sub(r'<h1.*>' + tag + '</h1>', '#' + tag, html)

    html = html.replace('<br />\n', '@@%%')
    html = html.replace('\n', '<br />')
    html = html.replace('&lt;br&gt;', '')
    html = html.replace('@@%%', '<br />')
    html = html.replace('@%@%', '\n')
    html = html.replace("@%", "\t")
    html = html.replace('<p>', "")
    html = html.replace('</p>', '')

    file2 = open(path, 'w', encoding='utf-8')
    file2.write(html)
    file2.close()


# 每次将 obsidian 导入 Anki 之前的第一步都是看看文件中有没有一级标题，如果没有，就先将文件名添加为文件的一级标题，之后再做后面的步骤。如果有，就用文件名覆盖一次一级标题，因为有可能一些文件名修改了，但一级标题还没有修改
# 日记文件不用添加一级标题
# 只有 文件名以 \d{14} 开头的需要添加一级标题
# 参数是读取的文件名和文件父目录的路径

def addH1Title(file, path):

    file1 = open(path + file, encoding='utf-8')
    conlist = file1.readlines()
    file1.close()

    if len(conlist) > 5:
        if not conlist[2].startswith('# '):
            conlist.insert(2, '# ' + file[:-3] + '\n')
            conlist.insert(3, '\n')

            file1 = open(path + file, 'w', encoding='utf-8')
            file1.writelines(conlist)
            file1.close()
        else:
            conlist[2] = '# ' + file[:-3] + '\n'

            file1 = open(path + file, 'w', encoding='utf-8')
            file1.writelines(conlist)
            file1.close()




# 将 question.txt 中的 <em>，</em> 转换为下划线，因为 latex 语法的下标是下划线，在之前的转换中被转换成了 <em> </em>。第一个下划线转换成 <em>，第二个下划线转换成 </em>
def changeEM2_(path):
    file4 = open(path, encoding='utf-8')
    context = file4.read()
    file4.close()

    context = context.replace('<em>', '_')
    context = context.replace('</em>', '_')

    file4 = open(path, 'w', encoding='utf-8')
    file4.write(context)
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



if __name__ == "__main__":

    # anki = [] # 用来存放那些即将导入anki的 问答题
    anki = ["aa@%", "bb@%", "cc@%@%"]
    article = ["aa@%", "bb@%", "cc@%@%"]

    path = 'c:\\Users\\john\\Documents\\zettelkasten2\\'  # 要处理的笔记目录

    htmlPath = 'C:\\Users\\john\\Downloads\\output.txt'
    questionPath = 'C:\\Users\\john\\Downloads\\question.txt'
    articlePath = 'C:\\Users\\john\\Downloads\\article.txt'
    anki_cloze_Path = 'C:\\Users\\john\\Downloads\\anki_cloze.txt'

    fileList = os.listdir(path)



    count = 0  # 用来计数，看看处理了多少个文件
    for file in fileList:

        count = count + 1
        print(count)

        # 如果是日记文件，就跳过，日记文件不放入 Anki 中
        if file.endswith('.md') and re.match(r'\d{8}', file) and len(file) == 11:
            continue
        
        if file.endswith('.md') and re.match(r'\d{14}', file):

            # addH1Title(file, path)

            file1 = open(path + file, encoding='utf-8')
            conlist = file1.readlines()
            file1.close()


            # 如果文件中有 dont_Anki 标签，那么这个文件就不用导入到 Anki 中
            if len(conlist) >= 1:
                if '#dont_Anki' in conlist[0]:
                    continue


            # 只将答案部分导入 Anki，文件的开头和 References 部分不导入
            conlist = conlist[3:]
            j = 0
            for j in range(len(conlist)):
                if conlist[j].startswith('## Reference'):
                    conlist = conlist[:j]
                    break
            

            aid = ''
            question = ''
            answer = ''

            i = 0
            for i in range(len(conlist)):
                if conlist[i] == '\n':
                    answer = answer + '<br>'
                elif conlist[i].startswith('Q：'): # 如果文件内容某行以 Q：开头，这个属于问题的一部分
                    question = conlist[i][2:-1]
                else:
                    answer = answer + conlist[i]


            aid = re.match(r'(\d{14})', file).group(1)
            question = file[15:-3] + '<br>' + question


            anki.append(aid + '@%') # @% 作为字段之间的分割
            anki.append(question + "@%")
            anki.append(answer + '@%@%') # @%@% 作为卡片之间的分割
            answer = ""

        # if file.endswith('.md') and not re.match(r'\d{14}', file):

        #     aid = ''
        #     question = ''
        #     answer = ''

        #     aid = file
        #     question = file

        #     file2 = open(path + file, encoding='utf-8')
        #     conlist = file2.readlines()
        #     file2.close()

        #     answer = "<br>".join(conlist)

        #     article.append(aid + '@%') # @% 作为字段之间的分割
        #     article.append(question + "@%")
        #     article.append(answer + '@%@%') # @%@% 作为卡片之间的分割
            
    
    
    markdown2htmlAndWrite2question(anki, questionPath)
    markdown2htmlAndWrite2question(article, articlePath)


    



    # 将图片、视频等复制到 anki 的媒体文件夹
    # 使用 freefilesync 来同步图片，这样更快
    # sdir = 'c:\\Users\\john\\Documents\\zettelkasten\\zltr\\'
    # ddir = 'C:\\Users\\john\\AppData\\Roaming\\Anki2\\账户1\\collection.media\\'
    copyMediaToAnki(questionPath)
    # copyMediaToAnki(articlePath, sdir, ddir)

    # 转换超链接
    turnHyperLink(questionPath)
    # turnHyperLink(articlePath)

    # 转换 latex
    turnBlockLatex(questionPath)
    turnInlineLatex(questionPath)

    # 将文件中的 <em>，</em> 转换为下划线
    changeEM2_(questionPath)
    # changeEM2_(articlePath)

    # 将文件中的 ~~ 变成 <del></del>
    turnDeleteLine(questionPath)
    # turnDeleteLine(articlePath)

    # 将 [[...]] 链接变成蓝色
    turnInlineLinkToRed(questionPath)
    # turnInlineLinkToRed(articlePath)

