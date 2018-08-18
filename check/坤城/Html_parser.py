# this time i need to add 幹支年在contents開頭位置
# 思路爲:找到前面的div如果沒有,就返回空字符串
# 如果有,直至找到第一個div爲止,將第一個div的內容取出. 如果第一個是圓圈或者三角,則替換爲空白,並將替換後的text的1-2位取出,返回
# bug1: 宣德九年三月戊寅朔 如果第一個幹支年不是['甲乙丙丁戊己庚辛壬癸']之中的一個,則向下搜索'朔'朔
# 如果找到了,則取前面的兩個,如果沒有找到,則返回''.
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
matches = [['坤城']]


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


# 返回幹支年
def find_old_year(cu_div):
    old_year = ''
    previous_d = cu_div.find_previous_sibling('div')
    if previous_d is None:
        return old_year
    else:
        while previous_d is not None:
            pre_pre_div = previous_d.find_previous_sibling('div')
            if pre_pre_div is None:
                pre_div_get_text = previous_d.get_text()
                pre_div_text_quanquan = [m.start() for m in re.finditer('○', pre_div_get_text)]
                pre_div_text_sanjiao = [m.start() for m in re.finditer('△', pre_div_get_text)]
                if len(pre_div_text_quanquan):
                    pre_div_get_text = pre_div_get_text.replace('○', '')
                elif len(pre_div_text_sanjiao):
                    pre_div_get_text = pre_div_get_text.replace('△', '')
                old_year = pre_div_get_text[0:2]
                old_year_first_match = [m.start() for m in re.finditer(old_year[0], '甲乙丙丁戊己庚辛壬癸')]
                if len(old_year_first_match):
                    return old_year
                else:

                    match = [m.start() for m in re.finditer('月', pre_div_get_text)]
                    if len(match):
                        p = match[0]
                        old_year = pre_div_get_text[p + 1:p + 3]
                        year_match = [m.start() for m in re.finditer(old_year[0], '甲乙丙丁戊己庚辛壬癸')]
                        if len(year_match):
                            return old_year
                        else:
                            return ''

            else:
                previous_d = pre_pre_div

fonts = soup.findAll('font', {'class': "hit0"})
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
            font_number_in_div = len(div.findAll('font', {'class': "hit0"}))
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
                        ganzhi_year = find_old_year(div)
                        # 查找是否當前div的前兩個字是幹支年,如果是,則不變,否則查找朔,如果有 則取前面兩個字,否則什麼都不變
                        current_div_year = div_get_text[0:2]

                        first_match = [m.start() for m in re.finditer(current_div_year[0], '甲乙丙丁戊己庚辛壬癸')]
                        if len(first_match):
                            pass
                        else:
                            if len(div_get_text) <= 20:
                                pass
                            else:
                                yue_match = [m.start() for m in re.finditer('月', div_get_text[0:20])]
                                if len(yue_match):
                                    position = yue_match[0]
                                    possible_old_year = div_get_text[position+1:position+3]
                                    old_year_match = [m.start() for m in re.finditer(possible_old_year[0], '甲乙丙丁戊己庚辛壬癸')]
                                    if len(old_year_match):
                                        div_get_text = possible_old_year+div_get_text[position+3:]

                        contents.append(ganzhi_year+div_get_text)
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
    worksheet.write(i, 0, matches[0][0])
    # worksheet.write(i, 1, heads_head[i])
    worksheet.write(i, 1, heads_contents[i])
    worksheet.write(i, 2, contents[i])
    ci_match_results = [m.start() for m in re.finditer('賜', contents[i])]
    if bool(len(ci_match_results)):
        worksheet.write(i, 3, 'bestow')
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
