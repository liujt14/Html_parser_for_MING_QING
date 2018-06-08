# -*- coding: utf-8 -*-

from selenium import webdriver 
brower = webdriver.Chrome()
brower.get('http://hanchi.ihp.sinica.edu.tw/mqlc/hanjishilu?2:342683590:10:/raid/ihp_ebook2/hanji/ttsweb.ini:::@SPAWN')
brower.implicitly_wait(8)

# <input type="IMAGE" name="_IMG_進階查詢" title="進階查詢" src="/mql/hanjishiluimg/adv.png" border="0">
brower.find_element_by_xpath("//input[@title='進階查詢']").click()
