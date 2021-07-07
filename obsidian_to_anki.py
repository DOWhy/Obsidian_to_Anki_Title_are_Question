# -*- coding: utf-8 

import markdown
import os
import sys
import re
import time
import document_content_process
import markdown2html
import file_properties

if __name__ == "__main__":

    # anki = [] # 用来存放那些即将导入anki的 问答题
    anki = []

    path = 'c:\\Users\\john\\Documents\\zettelkasten2\\'  # 要处理的笔记目录

    questionPath = 'C:\\Users\\john\\Downloads\\question.txt'

    fileList = os.listdir(path)

    count = 0  # 用来计数，看看处理了多少个文件
    for file in fileList:

        count = count + 1
        print(count)
        

        if re.match(r'\d{14}', file) and file.endswith('.md'):

        # TODO 文件属性修改时间，只处理某个时间之后的文件
            mtime = os.path.getmtime(path + file)
            lastTimeOfToAnki = file_properties.getLastTimeOfToAnki()

            if mtime > lastTimeOfToAnki:

                file1 = open(path + file, encoding='utf-8')
                conlist = file1.readlines()
                file1.close()

                # 如果文件中有 dont_Anki 标签，那么这个文件就不用导入到 Anki 中
                linenumberOfTags = document_content_process.getLinenumberOfTags(path + file)
                if linenumberOfTags != 'No tags:' and linenumberOfTags != '这是一个空文件':
                    if '#dont_Anki' in conlist[linenumberOfTags - 1]:
                        continue

                # 一级标题及之前，## References 及之后 都不导入 Anki
                linenumberOfH1title = document_content_process.getLinenumberOfH1title(path + file)
                linenumberOfReferences = document_content_process.getLinenumberOfReferences(path + file)
                if linenumberOfH1title != 'No H1title' and linenumberOfH1title != '这是一个空文件' and linenumberOfReferences != 'No ## References' and linenumberOfReferences != '这是一个空文件':
                    conlist = conlist[linenumberOfH1title:linenumberOfReferences-1]

                content = ''.join(conlist)
                html = markdown.markdown(content, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
                html = '@%@%' + html + '@%@%'
                html = file[0:14] + '\t' + file[15:-3] + '\t' + html + '\n'
                anki.append(html)

    file2 = open(questionPath, 'w', encoding='utf-8')
    file2.writelines(anki)
    file2.close()


    file_properties.saveTheTimeOfToAnki(time.time())


    markdown2html.turnInlineLinkToRed(questionPath)
    markdown2html.turnDeleteLine(questionPath)
    markdown2html.turnInlineLatex(questionPath)
    markdown2html.copyMediaToAnki(questionPath)


    # 将 question.txt 中的双引号都变成成对的双引号
    # 将 question.txt 中的 @%@% 变成双引号  # 因为用引号标明字段，所以字段内的引号要用成对的。见：https://docs.ankiweb.net/importing.html

    questionTxt = open(questionPath, encoding='utf-8')
    content = questionTxt.read()
    questionTxt.close()

    content = content.replace('"', '""')
    content = content.replace('@%@%', '"')

    questionTxt = open(questionPath, 'w', encoding='utf-8')
    questionTxt.write(content)
    questionTxt.close()