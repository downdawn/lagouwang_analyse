# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import urlencode
import time
from lxml import etree
import re
import pymongo


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
MONGO_URL = 'localhost'
MONGO_DB = 'lagouwang'
MONGO_COLLECTION = 'position'


def get_first_url(keyword, city):  # 请求搜索的第一页
    param = {
        "px": "default",
        "city": "{}".format(city),
    }
    url = "https://www.lagou.com/jobs/list_{}?".format(keyword) + urlencode(param)
    # print(url)
    browser.get(url)
    time.sleep(2)
    response = browser.page_source
    return response


def get_detail_link(response):  # 获取详情页的链接
    html = etree.HTML(response)
    url_list = html.xpath("//a[@class='position_link']/@href")
    for url in url_list:
        time.sleep(0.5)  # 请设置延时，不然会发现登录请求（可以解决，暂时搁置）
        parse_detail_page(url)


def parse_detail_page(url):  # 获取并解析职位信息
    browser.execute_script("window.open('"+url+"')")  # 打开一个新窗口
    browser.switch_to_window(browser.window_handles[1])  # 切换到该窗口
    wait.until(EC.presence_of_element_located((By.XPATH, "//dd[@class='job_bt']")))
    response = browser.page_source
    html = etree.HTML(response)
    title = html.xpath("//span[@class='name']/text()")[0]
    company = html.xpath("//h2[@class='fl']/text()")[0].strip()
    job_request_span = html.xpath("//dd[@class='job_request']//span")
    salary = job_request_span[0].xpath(".//text()")[0]
    salary = salary.strip()
    city = job_request_span[1].xpath(".//text()")[0]
    city = re.sub(r"[/\s]", "", city)
    work_years = job_request_span[2].xpath(".//text()")[0]
    work_years = re.sub(r"[/\s]", "", work_years)
    education = job_request_span[3].xpath(".//text()")[0]
    education = re.sub(r"[/\s]", "", education)
    welfare = html.xpath("//dd[@class='job-advantage']/p/text()")[0]
    company_website = html.xpath("//ul[@class='c_feature']/li[last()]/a/@href")[0]
    position_desc = "".join(html.xpath("//dd[@class='job_bt']/div//text()")).strip()
    position = {
        'title': title,  # 职位名称
        'city': city,  # 城市
        'salary': salary,  # 薪水
        'company': company,  # 公司名称
        'company_website': company_website,  # 公司主页
        'education': education,  # 学历要求
        'work_years': work_years,  # 工作经验
        'welfare': welfare,
        'desc': position_desc,  # 职位描述
        'origin_url': url  # 所属URL
    }
    browser.close()
    browser.switch_to_window(browser.window_handles[0])  # 获取信息完成后，再切换回第一个窗口
    save_position(position)
    # print(position)


def save_position(position):  # 保存职位信息
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    if collection.update({'origin_url': position['origin_url']}, {'$set': position}, True):  # 用url过滤更新
        print('保存到MongoDB成功：', position['origin_url'])
    else:
        print('保存到MongoDB失败：', position['origin_url'])


def main(keyword, city):
    response = get_first_url(keyword, city)
    num = 1
    while True:
        print("正在爬取第%s页" % num)
        num += 1
        get_detail_link(response)
        next_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'pager_next')]")))
        if "pager_next_disabled" in next_btn.get_attribute('class'):  # 判断是否有下一页
            print("全部爬取完毕！")
            browser.close()
            break
        next_btn.click()
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='item_con_list']/li")))  # 所有节点加载出来
        response = browser.page_source


if __name__ == '__main__':
    keyword = 'Python'  # 职位名称
    city = '深圳'  # 城市
    main(keyword, city)
