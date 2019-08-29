# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Firefox()
total_page = 10
urls = [f'https://search.jd.com/Search?keyword=python&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page={2*i-1}' for i in range(1,total_page+1)]
books = []

for url in urls:
    driver.implicitly_wait(3)#隐式等待
    driver.get(url)

    # 模拟下滑到底部操作
    for i in range(1, 5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    # 将加载好的页面源码给bs4解析
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # 进行信息的抽取（商品名称，价格）
    goods_info = soup.select(".gl-item")

    for info in goods_info:
        title = info.select(".p-name a em")
        price = info.select("div.p-price > strong > i")
        sku = info.get('data-sku')
        comment = info.select(".p-commit a")

        if info.select(".p-shopnum a"):
            publisher = info.select(".p-shopnum a")
        else:
            publisher = info.select(".p-shopnum")

        book = {'title':title[0].get_text(),
                'price':float(price[0].get_text()),
                'sku':'https://item.jd.com/' + info.get('data-sku') + '.html',
                'comment':comment[0].get_text(),
                'publisher':publisher[0].get_text().strip(),
                }
        books.append(book)

result = pd.DataFrame(books)[['title','price','sku','comment','publisher']].sort_values(['title','price'],ascending = [True,True])
writer = pd.ExcelWriter(r'C:\Users\xuelei\Desktop/京东_python.xlsx')
result.to_excel(writer,'Sheet1')
writer.save()

driver.close()