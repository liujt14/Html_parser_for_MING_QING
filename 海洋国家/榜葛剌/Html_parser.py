from bs4 import BeautifulSoup
import xlwt
import codecs
import re

page = codecs.open("./明實錄、朝鮮王朝實錄、清實錄資料庫合作建置計畫.html", 'r', 'utf-8')
soup = BeautifulSoup(page, "lxml")
contents = []
heads_all_contents = []
heads_head = []
heads_contents = []
K_number = []
matches = [['榜葛剌'], ['貢']]


def remove_tables_between_divs(table):
    previous_div = table.find_previous_sibling('div')
    next_div = table.find_next_sibling('div')
    if previous_div is None or next_div is None:
        table.decompose()
    else:
        previous_div_text = previous_div.get_text()
        next_div_text = next_div.get_text()
        if previous_div_text[0] == '○' or previous_div_text[0] == '△':
            if next_div_text[0] == '○' or next_div_text[0] == '△':
                table.decompose()
            else:
                next_div_contents = next_div.contents
                contents_list = []
                for content in next_div_contents:
                    contents_list.append(content)
                for content in contents_list:
                    previous_div.append(content)
                table.decompose()
                next_div.decompose()

tables = soup.find_all('table', {'class': "page2"})
for table in tables:
    remove_tables_between_divs(table)


def merge_div_to_one(div):
    div_string = div.get_text(strip=True)
    match_results = [m.start() for m in re.finditer('○', div_string)]
    match_t_results = [m.start() for m in re.finditer('△', div_string)]
    if len(match_results) or len(match_t_results):
        pass
    else:
        previous_div = div.find_previous_sibling('div')
        if previous_div is None:
            pass
        else:
            div_contents = div.contents
            contents_list = []
            for content in div_contents:
                contents_list.append(content)
            for content in contents_list:
                previous_div.append(content)
            div.decompose()
divs = soup.find_all('div')
for div in divs:
    merge_div_to_one(div)

fonts = soup.findAll('font', {'class': "hit"})
font_numbers = len(fonts)

k = 0
# 这里是一个循环

while k < font_numbers:
    div = fonts[k].find_parent('div')
    if div is None:
        k += 1
        pass
    else:
        div_string = div.get_text(strip=True)
        match_result = True

        for match in matches:
            if len(match) == 1:
                match_result_single = [m.start() for m in re.finditer(match[0], div_string)]
                match_result = bool(len(match_result_single)) and match_result
            else:
                sub_match_result = False
                for sub_match in match:
                    match_result_sub = [m.start() for m in re.finditer(sub_match, div_string)]
                    sub_match_result = bool(len(match_result_sub)) or sub_match_result
                match_result = sub_match_result and match_result
        if match_result:
            font_number_in_div = len(div.findAll('font', {'class': "hit"}))
            k += font_number_in_div
            # 向上搜索
            i = 0
            for parent in div.parents:
                if parent is None:
                    print(parent)
                else:
                    i += 1
                    if i >= 5 and parent.name == 'tr':
                        # 寻找兄弟节点
                        previous_tr = parent.find_previous_sibling('tr')
                        heads = previous_tr.get_text()
                        # heads optimal
                        heads_all_contents.append(heads)
                        div_get_text = div.get_text()
                        div_text_quanquan = [m.start() for m in re.finditer('○', div_get_text)]
                        div_text_sanjiao = [m.start() for m in re.finditer('△', div_get_text)]
                        if len(div_text_quanquan):
                            div_get_text = div_get_text.replace('○', '')
                        elif len(div_text_sanjiao):
                            div_get_text = div_get_text.replace('△', '')
                        contents.append(div_get_text)
                        K_number.append(k)

                    else:
                        pass
                if i > 6:
                    break
        else:
            k += 1

# save to excel:

workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('1st edition')

sheet_length = len(contents)
print("found %d rows before remove duplicate ones" % sheet_length)

# 去除重复的head,思路,遍历heads_contents 从1开始,如果当前index内容与前一个相同,那么删除当前index
# 对应的heads,并且将当前index的contents insert到上一个contents 并且删除当前index的contents
# index +1
index_for_heads = 1
while index_for_heads < sheet_length:
    if index_for_heads >= len(heads_all_contents):
        break
    else:
        if heads_all_contents[index_for_heads] == heads_all_contents[index_for_heads-1]:
            del heads_all_contents[index_for_heads]
            contents[index_for_heads-1] = contents[index_for_heads-1] + ';' + contents[index_for_heads]
            del contents[index_for_heads]
        index_for_heads += 1


sheet_length = len(contents)
print("found %d rows after remove duplicate ones" % sheet_length)

# for i in range(sheet_length):
#     if i == 0:
#         heads_all_contents.append()
for i in range(sheet_length):
    heads_match_results = [m.start() for m in re.finditer('／', heads_all_contents[i])]
    heads_head.append(heads_all_contents[i][0:heads_match_results[2]])
    heads_contents.append(heads_all_contents[i][(heads_match_results[2] + 1):])
    worksheet.write(i, 0, i+1)
    worksheet.write(i, 1, heads_head[i])
    worksheet.write(i, 2, heads_contents[i])
    worksheet.write(i, 3, contents[i])
file_name = 'Workbook'
for match in matches:
    if len(match) == 1:
        file_name += '_'
        file_name += match[0]

    else:
        for sub_match in match:
            file_name += '+'
            file_name += sub_match

workbook.save('./Excel_%s.xls' % file_name)
page.close()
