from bs4 import BeautifulSoup
import codecs
page = codecs.open("./明實錄、朝鮮王朝實錄、清實錄資料庫合作建置計畫.html", 'r', 'utf-8')

# 找到所有的font class=‘hit， 找到所有非重復的值.
# 能利用编码方式的差异自动生成matches变量吗?
soup = BeautifulSoup(page, "lxml")
fonts = soup.findAll('font', {'class': "hit"})
print("length of search words is: %d" % len(fonts))
fonts_set = {m.string for m in fonts if m.string is not None}
fonts_list = list(fonts_set)
print("search words list is : ")
print(fonts_list)
page.close()








# bug1: 如317所示，陕西和番僧所在的div中有一个table，所以不能被提取。
# bug2: 校准的内容在span里面，能不能把span去掉，然后将span的内容放到div里面？
# bug3: see number 39. 陕西被table的页数分开了。 能不能先去掉所有的table class= “page2” 然后将table所在位置的上一个div和下一个div合并成一个
# 再进行操作。 也可以解决bug1。注意：去掉table之后还会多出来一个没有string的font，这个个人觉得可以不处理。
# bug4: when there is no '○' in the div.get_text(), we need to span all the contents from next div to previous div
# bug5: add '△'
# bug6: 多型字的處理,比如說'陝西'or '陜西'

# 找到所有的font class=‘hit， 如果找到了font，找上一级的div
# 然后在div里面找到所有的font，记录font的值为n，
# 匹配陕西，番僧，匹配成功，有两步，第一，继续向上搜索
# 找到一个td 再找到一个tr-tbody--table--td--tr，然后找到一个并列的tr，把这个tr的text摘出来作为heads。第二步，将font所在的div的text摘出，作为contents。
# 然后开始找该div下一个div中的font。

# 找到所有的font class=‘hit， 如果找到了font，找上一级的div
# 然后在div里面找到所有的font，记录font的值为n，
# 匹配陕西，番僧，匹配成功，有两步，第一，继续向上搜索
# 找到一个td 再找到一个tr-tbody--table--td--tr，然后找到一个并列的tr，把这个tr的text摘出来作为heads。第二步，将font所在的div的text摘出，作为contents。
# 然后开始找该div下一个div中的font。

# 思路,在remove_all_tables之後進行tr的搜索,attribute爲bgcolor="whitesmoke" 然後找該tr的nexttr,然後找Next_tr所有的div.
# 如果沒有div,break 如果有div,做下個循環.
# 做循環,如果第一個div有o,則向下搜索,對每一個沒有o的div內容copy到上一個div.摧毀該div
# 如果第一個div沒有o,並且每個div都沒有o,則將所有的div放到第一個div上.摧毀除第一個div外所有div.


