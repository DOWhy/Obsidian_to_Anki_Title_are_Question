# -*- coding: utf-8 -*-

# 获取一级标题所在的行号
def getLinenumberOfH1title(path):

	file = open(path, encoding='utf-8')
	conlist = file.readlines()
	file.close()

	if len(conlist) == 0:
		return '这是一个空文件'

	i = 0
	for i in range(len(conlist)):
		if conlist[i].startswith('# '):
			return i+1

	return 'No H1title'


# 获取 ## References 所在的行号
def getLinenumberOfReferences(path):

	file = open(path, encoding='utf-8')
	conlist = file.readlines()
	file.close()

	if len(conlist) == 0:
		return '这是一个空文件'

	i = 0
	for i in range(len(conlist)):
		if conlist[i].startswith('## References'):
			return i+1

	return 'No ## References'


# 获取 tags: 所在的行号
def getLinenumberOfTags(path):

	file = open(path, encoding='utf-8')
	conlist = file.readlines()
	file.close()

	if len(conlist) == 0:
		return '这是一个空文件'

	i = 0
	for i in range(len(conlist)):
		if conlist[i].startswith('tags:'):
			return i+1

	return 'No tags:'


if __name__ == '__main__':

	path = 'C:\\Users\\john\\Documents\\python\\20210126145758 Anki 在代理下不能同步的解决方法.md'

	# linenumber = getLinenumberOfH1title(path)
	# linenumber = getLinenumberOfReferences(path)
	linenumber = getLinenumberOfTags(path)

	print(linenumber)