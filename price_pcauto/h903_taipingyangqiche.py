# -*- coding = utf-8 -*-
# @Time: 2022/10/28 16:54
"""
获取太平洋汽车品牌、型号、评论
"""
import requests
import time
import random
import os
import re
import json

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
                print('获取数据失败!', url)
        except Exception as e:
            print(url)
            print('出错了,正在重试...', e)
            if i == 9:
                with open('shibai.txt', 'w', encoding='utf-8') as f:
                    f.write(url + '\n')


def parse_data(res, file_name, url, re_list, index):
    # 使用xpath解析
    tree = etree.HTML(res.text)

    # 获取品牌 型号
    # mark_a_text_list = tree.xpath('//div[@class="pos-mark"]//text()')
    mark_a_list = tree.xpath('//*[@id="Jdoc"]/div/div[2]/div/div[2]/div/a')

    # 品牌
    position = mark_a_list[-2].xpath('./text()')[0]
    # 型号
    mark = mark_a_list[-1].xpath('./text()')[0]
    # print(position, mark)

    # 创建保存文件夹
    file_name = f'{file_name}/{position}-{mark}'
    if not os.path.exists(file_name):
        os.mkdir(file_name)

    # 获取封面图
    img_src = tree.xpath('//*[@id="Jdoc"]/div/div[2]/div/div[3]/div[2]/div[1]/a/img/@src')[0]

    # 获取封面图,保存
    # content = requests.get(img_src).content
    # img_name = f'{file_name}/{mark}.png'
    # with open(img_name, 'wb') as f:
    #     f.write(content)

    # 将品牌 型号 封面图写入文件
    with open('all_car.csv', 'a', encoding='utf-8') as f:
        f.write(f'{index},{position},{mark},{img_src}\n')

    div_list = tree.xpath('//div[@id="contentdivOnsale"]/div[2]/div')
    for div in div_list:
        dd_list = div.xpath('./dl/dd')

        # 逐项取出
        for dd in dd_list:
            tag_text = dd.xpath('./div[1]/p[1]/a/text()')
            if tag_text:
                tag_text = tag_text[0]

                # 不要2023款
                if '2023款' in tag_text:
                    continue

                # 获取参数href
                des_href = dd.xpath('./div[2]/a[1]/@href')
                if des_href:
                    des_href = des_href[0]
                    # 拼接href
                    des_href = urljoin(url, des_href)
                    des_href = des_href.split('#')[0]
                    if des_href in re_list:
                        continue
                    res = get_data(des_href)
                    parse_des(res, index, mark)
                    re_list.append(des_href)
                    return None


def parse_des(res, index, mark):
    # 使用正则获取数据
    pattern = r'"items":(.*?),"electricSg"'
    ret_list = re.findall(pattern, res.text)
    if ret_list:
        ret_list = ret_list[0]

        # 转成列表
        ret_list = json.loads(ret_list)

        # 保存数据列表
        save_value_list = []
        for i in range(len(ret_list[0]['ModelExcessIds'])+1):
            save_value_list.append([])

        for ret in ret_list:
            print(ret)
            name = ret['Name']
            print(name)
            # 过滤不需要的参数
            if ret['Item'] == '购车费用':
                continue
            if ret['Item'] == '耗能费用':
                continue

            save_value_list[0].append(ret['Name'])

            # 将获取到的数据保存到列表中
            for num, value_dic in enumerate(ret['ModelExcessIds']):
                save_value_list[num+1].append(value_dic['Value'])

        print(save_value_list)

        # 数据保存到文件
        with open(f'./car/{mark}.csv', 'w+', encoding='utf-8') as f:
            for value_list in save_value_list:
                print(value_list[0] + '保存成功!!!')
                f.write(str(index) + ',' + ','.join(value_list) + '\n')


def parse_comment(res):
    # 对应评论内容
    dic = {
        '用户名称': 'username',
        '购买时间': 'goumaishijian',
        '购买地点': 'goumaididian',
        '平均油耗': 'pingjunyouhao',
        '行驶里程': 'xingshilicheng',
        '优点': 'youdian',
        '缺点': 'quedian',
        '外观': 'waiguan',
        '内饰': 'neishi',
        '空间': 'kongjian',
        '配置': 'peizhi',
        '动力': 'dongli',
        '操控': 'caokong',
        '油耗': 'youhao',
        '舒适': 'shushi',
        '选车理由': 'xuancheliyou',
        '越野': 'yueye',
        '发表日期': 'fabiaoriqi',
        '购买车型': 'goumaichexing',
        '裸车价格': 'luochejiage',
        '外观评分': 'waiguanpingfen',
        '内饰评分': 'neishipingfen',
        '空间评分': 'kongjianpingfen',
        '配置评分': 'peizhipingfen',
        '动力评分': 'donglipingfen',
        '操控评分': 'caokongpingfen',
        '油耗评分': 'youhaopingfen',
        '舒适评分': 'shushipingfen'
    }

    # 存放评论列表
    pinglun_list = []

    # 使用xpath解析数据
    tree = etree.HTML(res.text)
    div_list = tree.xpath('//div[@class="scollbody"]/div')

    for div in div_list:
        pinglun_dic = {
            'username': '',
            'goumaishijian': '',
            'goumaididian': '',
            'pingjunyouhao': '',
            'xingshilicheng': '',
            'fabiaoriqi': '',
            'goumaichexing': '',
            'luochejiage': '',
            'waiguanpingfen': '',
            'neishipingfen': '',
            'kongjianpingfen': '',
            'peizhipingfen': '',
            'donglipingfen': '',
            'caokongpingfen': '',
            'youhaopingfen': '',
            'shushipingfen': '',
            'youdian': '',
            'quedian': '',
            'waiguan': '',
            'neishi': '',
            'kongjian': '',
            'peizhi': '',
            'dongli': '',
            'caokong': '',
            'youhao': '',
            'shushi': '',
            'xuancheliyou': '',
            'yueye': '',
        }

        # 用户名称
        username = div.xpath('./table/tr/td[1]/div/div[1]/div[1]/p/a/text()')
        if username:
            pinglun_dic['username'] = username[0]
        # 购买时间
        goumaishijian = div.xpath('./table/tr/td[1]/div/div[1]/div[3]/text()')
        if goumaishijian:
            pinglun_dic['goumaishijian'] = goumaishijian[0]
        # 购买地点
        goumaididian = div.xpath('./table/tr/td[1]/div/div[1]/div[4]/text()')
        if goumaididian:
            pinglun_dic['goumaididian'] = goumaididian[0]
        # 平均油耗
        pingjunyouhao = div.xpath('./table/tr/td[1]/div/div[1]/div[6]/i/text()')
        if pingjunyouhao:
            pinglun_dic['pingjunyouhao'] = pingjunyouhao[0]
        # 行驶里程
        xingshilicheng = div.xpath('./table/tr/td[1]/div/div[1]/div[7]/text()')
        if xingshilicheng:
            pinglun_dic['xingshilicheng'] = xingshilicheng[0]
        # 发表时间
        fabiaoriqi = div.xpath('./table/tr/td[1]/div/div[1]/div[1]/span/a/text()')
        if fabiaoriqi:
            pinglun_dic['fabiaoriqi'] = fabiaoriqi[0]
        # 购买车型
        goumaichexing = div.xpath('./table/tr/td[1]/div/div[1]/div[2]/a/text()')
        if goumaichexing:
            pinglun_dic['goumaichexing'] = goumaichexing[0]
        # 裸车价格
        luochejiage = div.xpath('./table/tr/td[1]/div/div[1]/div[5]/i/text()')
        if luochejiage:
            pinglun_dic['luochejiage'] = luochejiage[0]
        # 外观评分
        waiguanpingfen = div.xpath('./table/tr/td[1]/div/div[2]/ul/li[1]/b/text()')
        if waiguanpingfen:
            pinglun_dic['waiguanpingfen'] = waiguanpingfen[0]
        # 内饰评分
        neishipingfen = div.xpath('./table/tr/td[1]/div/div[2]/ul/li[2]/b/text()')
        if neishipingfen:
            pinglun_dic['neishipingfen'] = neishipingfen[0]
        # 空间评分
        kongjianpingfen = div.xpath('./table/tr/td[1]/div/div[2]/ul/li[3]/b/text()')
        if kongjianpingfen:
            pinglun_dic['kongjianpingfen'] = kongjianpingfen[0]
        # 配置评分
        peizhipingfen = div.xpath('./table/tr/td[1]/div/div[2]/ul/li[4]/b/text()')
        if peizhipingfen:
            pinglun_dic['peizhipingfen'] = peizhipingfen[0]
        # 动力评分
        donglipingfen = div.xpath('./table/tr/td[1]/div/div[2]/ul/li[5]/b/text()')
        if donglipingfen:
            pinglun_dic['donglipingfen'] = donglipingfen[0]
        # 操控评分
        caokongpingfen = div.xpath('./table/tr/td[1]/div/div[2]/ul/li[6]/b/text()')
        if caokongpingfen:
            pinglun_dic['caokongpingfen'] = caokongpingfen[0]
        # 油耗评分
        youhaopingfen = div.xpath('./table/tr/td[1]/div/div[2]/ul/li[7]/b/text()')
        if youhaopingfen:
            pinglun_dic['youhaopingfen'] = youhaopingfen[0]
        # 舒适评分
        shushipingfen = div.xpath('./table/tr/td[1]/div/div[2]/ul/li[8]/b/text()')
        if shushipingfen:
            pinglun_dic['shushipingfen'] = shushipingfen[0]

        inner_div_list = div.xpath('./table/tr/td[2]/div/div[2]/div')
        for inner_div in inner_div_list:
            text = inner_div.xpath('./b/text()')[0].replace('：', '')

            pinglun_dic[dic[text]] = inner_div.xpath('./span/text()')[0]

        pinglun_list.append(pinglun_dic)
    # print(pinglun_list)

    with open('pinglun.csv', 'a', encoding='utf-8') as f:
        for pinglun_dic in pinglun_list:
            print(pinglun_dic)
            f.write(','.join([value for value in pinglun_dic.values()]) + '\n')


def main():
    # 去重列表
    re_list = []
    if os.path.exists('re_url.txt'):
        with open('re_url.txt', 'r', encoding='utf-8') as f:
            for one_url in f.readlines():
                re_list.append(one_url.strip())

    # 创建保存车品牌 型号的csv
    if not os.path.exists('all_car.csv'):
        with open('all_car.csv', 'w', encoding='utf-8') as f:
            f.write('序号,品牌,型号,图片链接\n')

    # 创建保存评论的csv文件
    if not os.path.exists('pinglun.csv'):
        with open('pinglun.csv', 'w', encoding='utf-8') as f:
            f.write('用户名称,购买时间,购买地点,平均油耗,行驶里程,发表日期,购买车型,裸车价格,外观评分,内饰评分,空间评分,配置评分,动力评分,操控评分,油耗评分,舒适评分,优点,缺点,外观,内饰,空间,配置,动力,操控,油耗,舒适,选车理由,越野\n')

    # 创建保存文件夹
    file_name = 'price'
    if not os.path.exists(file_name):
        os.mkdir(file_name)

    # 需要爬取的车的url
    car_url_list = [
        'https://price.pcauto.com.cn/price/sg9550/',  # 奥迪A3
        'https://price.pcauto.com.cn/price/sg3524/',  # 奥迪A4L
        'https://price.pcauto.com.cn/price/sg4313/',  # 奥迪A6L
        'https://price.pcauto.com.cn/price/sg5/',  # 奥迪A4(进口)
        'https://price.pcauto.com.cn/price/sg4438/',  # 奥迪A5
        'https://price.pcauto.com.cn/price/sg6/',  # 奥迪A6(进口)
        'https://price.pcauto.com.cn/price/sg3776/',  # 奥迪A7
        'https://price.pcauto.com.cn/price/sg7899/',  # 奥迪RS 4
        'https://price.pcauto.com.cn/price/sg9301/',  # 凌派
        'https://price.pcauto.com.cn/price/sg22951/',  # 奔驰A级
        'https://price.pcauto.com.cn/price/sg3178/',  # 奔驰C级
        'https://price.pcauto.com.cn/price/sg1603/',  # 奔驰E级
        'https://price.pcauto.com.cn/price/sg20583/',  # 宝马1系
        'https://price.pcauto.com.cn/price/sg424/',  # 宝马3系
        'https://price.pcauto.com.cn/price/sg441/',  # 宝马5系
        'https://price.pcauto.com.cn/price/sg3188/',  # 凯越
        'https://price.pcauto.com.cn/price/sg4437/',  # 高尔夫
        'https://price.pcauto.com.cn/price/sg28071/',  # 锋兰达
        'https://price.pcauto.com.cn/price/sg10740/',  # 福睿斯
        'https://price.pcauto.com.cn/price/sg24885/',  # 凯迪拉克CT5
        'https://price.pcauto.com.cn/price/sg22673/',  # 途达
        'https://price.pcauto.com.cn/price/sg14263/',  # 悦纳
        'https://price.pcauto.com.cn/price/sg24483/',  # 创界
    ]

    flag = True

    try:
        index = 0
        # 取出每一个url,发送请求
        for url in car_url_list:
            index += 1
            if url in re_list:
                flag = False

            if flag:
                res = get_data(url)
                # print(res.text)

                # 解析数据
                parse_data(res, file_name, url, re_list, index)
                re_list.append(url)

            # 获取评论
            url_list = url.split('.')
            url_list[-1] = url_list[-1].replace('price', 'comment')

            for page in range(1, 100):
                url = '.'.join(url_list)
                url = url + f'p{page}.html'
                if url in re_list:
                    continue
                res = get_data(url)
                parse_comment(res)
                re_list.append(url)

    except Exception as e:
        print('出错了:', e)

    finally:
        with open('re_url.txt', 'w', encoding='utf-8') as f:
            for one_url in re_list:
                f.write(one_url + '\n')


if __name__ == '__main__':
    main()
