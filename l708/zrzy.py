# -*- coding = utf-8 -*-
# @Time: 2022/10/16 13:20
import requests
import time
import random
from lxml import etree
import re
from urllib.parse import urljoin
import sys
import os


def done_url():
    done_url_list = []

    # 获取已完成的url存放到done_list中
    with open('1.txt', 'r', encoding='utf-8') as f:
        for url in f.readlines():
            if url.startswith('请求成功:'):
                # print(url.split(':', 1)[-1].replace('\n', ''))
                done_url_list.append(url.split(':', 1)[-1].replace('\n', ''))

    return done_url_list


def get_data(url, method, data):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    for i in range(10):
        try:
            # get
            if method == 'get':
                res = requests.get(url, headers=headers, timeout=10)

            # post
            else:
                res = requests.post(url, headers=headers, data=data, timeout=10)
            time.sleep(random.choice([4, 5, 6]))
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


def parse_save_data(res):
    # 使用xpath获取数据
    tree = etree.HTML(res.text)
    # 行政区
    xingzhengqu = tree.xpath('//*[@id="XZQ_DM"]/text()')
    if xingzhengqu:
        xingzhengqu = xingzhengqu[0]
    # 项目名称
    xiangmumingcheng = tree.xpath('//*[@id="XM_MC"]/text()')
    if xiangmumingcheng:
        xiangmumingcheng = xiangmumingcheng[0]
    # 项目位置
    xiangmuweizhi = tree.xpath('//*[@id="TD_ZL"]/text()')
    if xiangmuweizhi:
        xiangmuweizhi = xiangmuweizhi[0]
    # 合同编号
    hetongbianhao = tree.xpath('//*[@id="BH"]/text()')
    if hetongbianhao:
        hetongbianhao = hetongbianhao[0]
    # 面积
    mianji = tree.xpath('//*[@id="GY_MJ"]/text()')
    if mianji:
        mianji = mianji[0]
    # 行业分类
    hangyefenlei = tree.xpath('//*[@id="HY_FL"]/text()')
    if hangyefenlei:
        hangyefenlei = hangyefenlei[0]
    # 土地使用权人
    tudishiyongren = tree.xpath('//*[@id="SRR"]/text()')
    if tudishiyongren:
        tudishiyongren = tudishiyongren[0]
    # 约定开工时间
    yuedingkaigongshijian = tree.xpath('//*[@id="DG_SJ"]/text()')
    if yuedingkaigongshijian:
        yuedingkaigongshijian = yuedingkaigongshijian[0]
    # 批准单位
    pizhundanwei = tree.xpath('//*[@id="PZ_JG"]/text()')
    if pizhundanwei:
        pizhundanwei = pizhundanwei[0]
    # 约定交地时间
    yuedingjiaodishijian = tree.xpath('//*[@id="JD_SJ"]/text()')
    if yuedingjiaodishijian:
        yuedingjiaodishijian = yuedingjiaodishijian[0]
    # 预定竣工时间
    yudingjungongshijian = tree.xpath('//*[@id="JG_SJ"]/text()')
    if yudingjungongshijian:
        yudingjungongshijian = yudingjungongshijian[0]
    # 签订日期
    qiandingriqi = tree.xpath('//*[@id="QD_RQ"]/text()')
    if qiandingriqi:
        qiandingriqi = qiandingriqi[0]

    # 20200101前数据终止程序
    qiandingriqi2 = int(qiandingriqi.replace('-', ''))
    if qiandingriqi2 < 20200101:
        sys.exit()

    print(xingzhengqu, xiangmumingcheng, xiangmuweizhi, hetongbianhao, mianji, hangyefenlei, tudishiyongren,
          yuedingkaigongshijian, pizhundanwei, yuedingjiaodishijian, yudingjungongshijian, qiandingriqi)

    # 数据写入文件
    with open('info.csv', 'a', encoding='utf-8') as f:
        f.write(f'{xingzhengqu}, {xiangmumingcheng}, {xiangmuweizhi}, {hetongbianhao}, {mianji}, {hangyefenlei}, {tudishiyongren}, {yuedingkaigongshijian}, {pizhundanwei}, {yuedingjiaodishijian}, {yudingjungongshijian}, {qiandingriqi}\n')


def main():
    # 存放已完成url
    # done_list = done_url()

    # 新建存放数据文件,写入表头
    if not os.path.exists('info.csv'):
        with open('info.csv', 'w', encoding='utf-8') as f:
            f.write(f'行政区, 项目名称, 项目位置, 合同编号, 面积(公顷), 行业分类, 土地使用权人, 约定开工时间, 批准单位, 约定交地时间, 约定竣工时间, 签订日期\n')

    # 逐页发送post请求
    for start in range(1, 85):
        print(f'开始获取第{start}页!')
        url = 'http://zrzy.jiangsu.gov.cn/gtapp/xxgk/tdsc_getGdxmList.action'
        data = {
            'start': start,
            'limit': 25,
            'xzqhdm': 320600,
            'lx': '21,22,23',
            'affiche_no': '',
            'remise_type': '',
            'starttime': '',
            'endtime': ''
        }
        res = get_data(url, 'post', data)
        # print(res.text)

        # 正则获取所有url
        pattern = r'<a href=\\"(.*?)\\" target=_blank'
        href_list = re.findall(pattern, res.text)

        if not len(href_list) == 25:
            print(f'{start}不足25!')

        for href in href_list:
            href = urljoin(url, href)

            # 去重
            # if href in done_list:
            #     continue

            # 发送请求,获取数据
            res = get_data(href, 'get', None)
            # print(res.text)

            # 解析数据
            parse_save_data(res)

            # 将url添加到已完成列表
            # done_list.append(href)


if __name__ == '__main__':
    main()
