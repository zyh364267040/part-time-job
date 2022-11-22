# -*- coding = utf-8 -*-
# @Time: 2022/11/22 11:32
"""
获取拼多多商品折扣信息
https://pifa.pinduoduo.com/search?cate=9586&level=2
"""
import requests
import time
import random


def get_data(url, data=None):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'referer': 'https://pifa.pinduoduo.com/search?cate=9586&level=2',
        'cookie': '_nano_fp=XpEjlp9Jn5ConqmYXo_lWwMRXnR6gxwtur~aorDi; VISITOR_PASS_ID=cTMWIy7LGHRqJp9ZqlLBFTW7ow0ybyCYdpi93Ez8zGHUSP8KAgaRPzaB4hCFHCZwgEH45blInMdi75ewpEvDb49ncnWtrS-9dxGoh8kTZbQ_f652adee4f; api_uid=CgpsEGN8PlhWlggQGiQuAg==; webp=true; _bee=ChMneRua4Qzm5ovuL9ztih0sDYvUREQv; _f77=55aaaa73-6f0b-48eb-a2f1-0817e1363009; _a42=c62d633a-af8d-4846-8389-a1a1307f7b6e; rckk=ChMneRua4Qzm5ovuL9ztih0sDYvUREQv; ru1k=55aaaa73-6f0b-48eb-a2f1-0817e1363009; ru2k=c62d633a-af8d-4846-8389-a1a1307f7b6e',
        'content-type': 'application/json',
        'anti-content': '0aqAfxUeMwCEBKbPDA9ewGYolRW22-9U9XaxIvWdgD6Wq2U6Ocg3UFCxMqCq4ETEaDGelEpPgEWqYpMRq2B9NOm3ZNCxZoMfmqpBUbGX-xU7ORNBXpEqrqWAwREaDtQRmPdPlX_qYGMeq0Bs3eB3Kk1TXeyjCuXdyBXUkaSMvk0B4uEcYgu90shOI3FhC15QBfuYQTBx6UBhK41kwITNTGPM9sZYBWk42Q30Bnyp9mq7CPemqBXZdq6PPxsptuCUgmTxMtMSq4Big_cpd2LHuesPG-9RYlTc00lt4F1tGD_jqVPpgodtNUX_qSn2qti3QxmVAGdxtGF0QoFxffdzycp4YljSn_qj2xDPaD-1wQu6wHbQrsrq2FkB15DBwKEzfCeBZhez2HKB1IezwKkzvKEB3IeBCEylgwPHsz3Ss5ezv-Kz-6IMjRvMelpIBRIeL4CbehESf-7F-RmEkJCMvA_MIX9ss0a0jkPd09y50myUpW7v69OtXZf0dinNObOypmjncmYn-QTNQEPNW7wdmUfYg3vmginYOr7v60ltXHQpud6lF7Q99TvCZQpgKOqKvKkn4Pt7Gnq45qiNFquNVXtmqXUNhnYaOciCqGqCOY_tN1G_KoIgolG70Pr5sk3TXP3ok0EjuJQP59SPYaSQpJTQplaj06ujSE-rYDB-HSG6DXhX999Kdoq9pSSsNPV',
        'origin': 'https://pifa.pinduoduo.com',
    }
    for i in range(10):
        try:
            if not data:
                res = requests.get(url, headers=headers, timeout=10)
            else:
                res = requests.post(url, headers=headers, timeout=10, data=data)
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


def post_data():
    url = 'https://pifa.pinduoduo.com/pifa/search/searchOptGoods'
    data = {

    }


def main():
    url = 'https://pifa.pinduoduo.com/pifa/search/searchOptGoods'
    page = 2
    data = {
        'level': 2,
        'optId': 9586,
        'page': page,
        'propertyItems': [],
        'rn': "4335b25c-d16b-4fae-ba43-88c80f535a61",
        'size': 20,
        'sort': 0,
        'url': ""
    }
    res = get_data(url, data=data)
    print(res.text)


if __name__ == '__main__':
    main()
