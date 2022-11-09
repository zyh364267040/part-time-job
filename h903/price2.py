# -*- coding = utf-8 -*-
# @Time: 2022/10/31 21:51
import requests
import time
import random
import re

from lxml import etree
from urllib.parse import urljoin


def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    for i in range(10):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            time.sleep(random.choice([2, 3, 4]))
            if res and res.status_code == 200:
                print(f'请求成功:{url}')
                return res
            else:
                print('获取数据失败!')
        except Exception as e:
            print(url)
            print('出错了,正在重试...', e)
            if i == 9:
                with open('shibai.txt', 'w', encoding='utf-8') as f:
                    f.write(url + '\n')


def parse_data(res, url):
    # 使用xpath获取数据
    res_text = res.text.strip(';').strip('document.getElementById("tree").innerHTML=\'')
    tree = etree.HTML(res_text)
    li_list = tree.xpath('//li')

    # 汽车名首字母
    letter = ''
    for li in li_list:
        letter_list = li.xpath('./text()')
        if letter_list:
            letter = letter_list[0]
            continue

        # 汽车链接
        href = li.xpath('./a[2]/@href')
        if href:
            href = urljoin(url, href[0])

        # 汽车名称
        title = li.xpath('./a[2]/@title')
        if title:
            title = title[0]

        # 发送请求,获取每一个品牌汽车信息
        one_car_res = get_data(href)
        parse_one_car_data(one_car_res, href, letter, title)

        print(letter, title, href)


def parse_one_car_data(res, url, letter, title):
    # print(res.text)

    # 使用正则匹配封面图片链接
    pattern = r'#src="(.*?)">'
    result = re.findall(pattern, res.text)

    # 使用xpath解析数据
    tree = etree.HTML(res.text)
    div_list = tree.xpath('//div[@id="JlistTb"]/div')

    i = 0
    for div in div_list:
        name = div.xpath('./div/p[2]/a/text()')
        href = div.xpath('./div/p[2]/a/@href')
        if href:
            href = urljoin(url, href[0])
            img_res = get_data(href)
            img_list = parse_img_data(img_res)
            img = result[i]
            img_list.append(img)
            name = name[0]
            data = f'{letter},{title},{name},{img_list[0]}'
            for img in img_list:
                data += ',' + img

            print(data)
            with open('car_info.csv', 'a', encoding='utf-8') as f:
                f.write(
                    data + '\n'
                )
            i += 1


def parse_img_data(res):
    img_list = []
    # 使用xpath解析
    tree = etree.HTML(res.text)
    a_list = tree.xpath('//*[@id="JfocusPlst"]/div[1]/div[3]/a')
    i = 0
    for a in a_list:
        src = a.xpath('./img/@src2')
        if src:
            src = src[0]
            img_list.append(src)
            i += 1
        if i == 3:
            break

    return img_list


def main():
    # 创建存储文件
    with open('car_info.csv', 'w', encoding='utf-8') as f:
        f.write(
            '汽车名首个汉字字母,品牌,汽车名字,封面图链接,图片1,图片2,图片3\n'
        )
    # url = 'https://price.pcauto.com.cn/'
    url = 'https://price.pcauto.com.cn/index/js/5_5/treedata-cn-html.js?t=6'

    res = get_data(url)
    parse_data(res, url)


if __name__ == '__main__':
    main()
