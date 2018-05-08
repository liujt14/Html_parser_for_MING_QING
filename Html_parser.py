from bs4 import BeautifulSoup
import xlwt
import codecs
import re

page = codecs.open("./明實錄、朝鮮王朝實錄、清實錄資料庫合作建置計畫.html", 'r', 'utf-8')
soup = BeautifulSoup(page, "lxml")
contents = []
heads_head = []
heads_contents = []
K_number = []
matches = [['朵顏衞', '朶顏衞','朵顏衛','朶顏衛']]


def remove_table_and_merge_div(font):
    if font.get_text() == "\n":
        div = font.find_parent('div')
        table = div.find_previous_sibling('table')
        table.decompose()
        current_div_contents = div.get_text()
        previous_div = div.find_previous_sibling('div')
        previous_div.append(current_div_contents)
        div.decompose()


def remove_tables_between_divs(table):
    previous_div = table.find_previous_sibling('div')
    next_div = table.find_next_sibling('div')
    if previous_div is None or next_div is None:
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


fonts = soup.find_all('font', {'class': "hit"})
for font in fonts:
    if font.string is None:
        remove_table_and_merge_div(font)
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
        break
    div_string = div.get_text(strip=True)
    # match1_results = [m.start() for m in re.finditer(match1, div_string)]
    # match1_another_results = [m.start() for m in re.finditer(match1_another, div_string)]
    # match2_results = [m.start() for m in re.finditer(match2, div_string)]
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
    # if len(match1_results) or len(match1_another_results) and len(match2_results):
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
                    heads_match_results = [m.start() for m in re.finditer('／', heads)]
                    heads_head.append(heads[0:heads_match_results[2]])
                    heads_contents.append(heads[(heads_match_results[2]+1):])
                    div_get_text = div.get_text()
                    if div_get_text[0] == '○' or div_get_text[0] == '△':
                        div_get_text = div_get_text.replace(div_get_text[0],'')
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
print("found %d rows" % sheet_length)
for i in range(sheet_length):
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
