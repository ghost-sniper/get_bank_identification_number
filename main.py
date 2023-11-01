# 这是一个示例 Python 脚本。
import json

import requests
from lxml import etree

bin_list = []


class Bin:
    pass


def get_bin_info(bin_url):
    bin_res = requests.get(bin_url)
    if str(bin_res) == '<Response [404]>':
        return
    bin_html = bin_res.text
    bin_element = etree.HTML(bin_html)
    print(bin_url)
    bin_list_node = bin_element.xpath('//html/body/section[1]/section[3]/div/div/table/tbody')[0]
    # print(bin_list_node)
    bin_infos = bin_list_node.xpath('./tr')
    for info in bin_infos:
        details = info.xpath('./td')
        bin_info = Bin
        bin_info.number = details[0].xpath('./b/a')[0].text.split(' ')[0]
        bin_info.country = details[1].xpath('./a')[0].text.split(' ')[0]
        bin_info.name = details[2].xpath('./a')[0].text
        bin_info.brand = details[3].xpath('./a')[0].text.split(' ')[0]
        bin_info.type = details[4].text.strip()
        bin_info.level = details[5].text.strip()
        bin_list.append(bin_info)
        # for i in bin_list:
        #     print(i.number)
        #     print(i.country)
        #     print(i.name)
        #     print(i.brand)
        #     print(i.type)
        #     print(i.level)
        # while i < len(details):
        #
        #     if i == 0:
        #         print('%s \t' % details[i].xpath("./b/a")[0].text)
        #         s = details[i].xpath('./b/a')[0].text
        #         bin_info.number = s.split(' ')[0]
        #     elif i < 4:
        #         print('%s \t' % details[i].xpath('./a')[0].text)
        #     elif i == 4:
        #         print('%s \t ' % details[i].text)
        #     else:
        #         print('%s \n' % details[i].text)
        #     i = i + 1


# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
def get_bin_list(child_url):
    country_res = requests.get(child_url)
    country_html = country_res.text
    bank_element = etree.HTML(country_html)
    bank_nodes = bank_element.xpath('//html/body/section/section[2]/div/div[4]/a')
    for bank_node in bank_nodes:
        # print(bank_node.attrib['href'])
        get_bin_info(bank_node.attrib['href'])
        # bank = bank_node.xpath('./div[2]/h3')
        # print(bank[0].text)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    res = requests.get('https://bincheck.io/zh/bin-list')
    html = res.text
    # print(html)
    element = etree.HTML(html)
    nodes = element.xpath('//html/body/section/section/div/div[2]/a')
    for node in nodes:
        # print(node.attrib['href'])
        country = node.xpath('./div[2]/h3')
        # print(country[0].text)
        get_bin_list('https://bincheck.io/zh' + node.attrib['href'])
    s = json.dumps(bin_list)
    print(s)
    with open('/bin.json') as f:
        json.dump(bin_list, f)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
