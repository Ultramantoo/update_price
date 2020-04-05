# coding=utf-8

import requests
import json
import xlwings as wx
import common
import requests_sides
import sys
import schedule
import time
import re
import csv
import base64

from PIL import Image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# import urllib.parse

"""
用类，来体现
1.打开选择导入表格
2.读取配置信息
3.爬取数据信息
4.分析数据信息
5.写入归档数据信息
后期
增加 优惠价格判断
增加 优惠价格微信邮件短信提醒
2020-01-08
获取商品的购买链接
获取商品的 uid值
自动跳转到商品链接，完成自动锁单
    注意自动判断否海淘额度
    自动判断商品价格是否一致
    自动判断身份证与收货人名一致
2020-1-18
1. 增加购买记录与发送记录 【急】 ok
2. 测试多线程购买【cookies】 是否被通用 暂 先稳定性
3. 测试去掉print 优化提醒  【急】ok
4. 增加 额度查询验证 ok
5. 测试一轮完整流程后，初步上线，测试稳定性！！ 【急】 ok
6. 先发送提醒，再自动锁单 【急】 ok

++++++++++++++++
2020031
1、自动更新额度
2、多线程购买
3、返利页面购买
4、更高级的定时任务
"""

# noinspection PyBroadException,PyAttributeOutsideInit,SpellCheckingInspection
class GetPrice(object):
    def __init__(self):
        self.field_dic_list = []
        self.initial_table = []
        self.send_value_save_id = []
        # 购物车
        self.cookies_oj = [
            {'domain': '.amazon.cn', 'expiry': 2082729601.413418, 'httpOnly': False, 'name': 'x-wl-uid', 'path': '/',
             'secure': False,
             'value': '1WUcXQ1W96p2Da+K/0Rh70IrEBk11UtAZMZ/BqtGcaq78/7WuLVwClAIoJN/XD3t/j1NV/+4nJIGTSe55o5XiOQZ34zCGxXUTHCMAzxnbYbqjL9xhT4mNOKVHE2bLJfBl7LmwKEWQjac='},
            {'domain': '.amazon.cn', 'expiry': 2209772928.051648, 'httpOnly': True, 'name': 'at-main', 'path': '/',
             'secure': True,
             'value': 'Atza|IwEBIN5oeMxme6hizXITwVIA18jENhcgmpK3viYQq3bP05F6304zJOuBCd0EOENVDMGICpbnOAGW6dRVBwEtejBhi0yhOcexWJ1JQr6nIrm3IvmmNKXcyoVEMJSJLhymW83hZj-w_AnSPHFajFqWQlEl8VXQw3NLFrkNVIFe1ifwDyy58jyOFYqWozluwiqtyANc3EWdX8paCiCupsEtelnrBlyVZPk2e-BKHbcxXf8tCncFBVshzx8IDlCXKQaJxTTvgXxzpez3a9hNpyYWUddjMl9TlmLy1rCj3dxVPTo9mHuP_jfJBeOkt-QJO6WqUwYORoL6fwAYnulH7AIWN0kjzsz6-E4UcPNU9ix84-cOJzI0t9kouEC199QW1kRfNgFnWRlL3OBDmIEs-BRV5MRTE-7k'},
            {'domain': '.amazon.cn', 'expiry': 2209772928.051544, 'httpOnly': False, 'name': 'session-token',
             'path': '/', 'secure': False,
             'value': '"Vz9fmhw9mSikg5GV1UYTeoKv2raQc8fmKFmlmtkElR046D1cj44vG5jSgZBK0Yg4qS6RRcSEU9KkZUPdxddHsIBOqsZfmH3wMpNdFjr+VqQ31Qb6Su1K268vbPh8KtmlT0074aChAGLyZHXB4GRSRn675EeE1yChEr8Ks59PPhlkR2xYrGjju+wxQFda1f8TKKt0FgRK+RO4lBGGX5hQYzkh7PFMiMx2Q03gGZnVV187O7aZjQBRusCy5QB5IqyoxFg+/Otuazs="'},
            {'domain': '.amazon.cn', 'expiry': 2209772928.051607, 'httpOnly': False, 'name': 'x-acbcn', 'path': '/',
             'secure': False, 'value': 'NXzEuqje8oFyN9Jlsoyrce0cKirl7MFsqSWmIvL0AaLgwLQkcxmqqqMgESenKtEt'},
            {'domain': '.amazon.cn', 'expiry': 2209772928.051702, 'httpOnly': True, 'name': 'sess-at-main', 'path': '/',
             'secure': True, 'value': '"hFL/KrWJKDApr4UXiwx8v4HjnYONog/MmzCQNwJ/2hg="'},
            {'domain': '.amazon.cn', 'expiry': 2082729601.53402, 'httpOnly': False, 'name': 'ubid-acbcn', 'path': '/',
             'secure': False, 'value': '457-1642996-6165231'},
            {'domain': '.amazon.cn', 'expiry': 2209772928.051741, 'httpOnly': True, 'name': 'sst-main', 'path': '/',
             'secure': True,
             'value': 'Sst1|PQFBbxQc2TEGT1dsVyAwVlsCCwhTucNM6RPIwMUuEuzMrK0OoyK6zMRLXtE01l4ZF0HMhzxEckvv4rKv5KS2f35POXm2pRjwnHPAG3NQLx6efwiS4Ekejrj-ue2LQBvXzDx3XB7lbwbeGUvZ3UPqF54hAFnKsVE-zQ8KWVyTmIFnmex__XpMsJLTKnL2kNrzdR837lZ4pyDv7_076ggXFELILMEdTSCYaXHst5v7E6DSyxZGbd8X5YZgJFkTjXZR0r-RzNLAyI3KtDqbTcqxnnrt67W9JyyHNUZcYk1fIxTFyUgByZ3coPlobWIX4I_uY6pzirZpeH_xBzCzqgt10JR-ZA'},
            {'domain': '.amazon.cn', 'expiry': 2082729601.534049, 'httpOnly': False, 'name': 'session-id-time',
             'path': '/', 'secure': False, 'value': '2082729601l'},
            {'domain': 'www.amazon.cn', 'expiry': 1610588913, 'httpOnly': False, 'name': 'cnm_gw_cnffpe_c2',
             'path': '/', 'secure': False, 'value': '1579052910000'},
            {'domain': '.amazon.cn', 'expiry': 1579053768.0514, 'httpOnly': False, 'name': 'a-ogbcbff', 'path': '/',
             'secure': False, 'value': '1'},
            {'domain': '.amazon.cn', 'expiry': 2082729601.534075, 'httpOnly': False, 'name': 'session-id', 'path': '/',
             'secure': False, 'value': '461-9135040-8826352'},
            {'domain': 'www.amazon.cn', 'expiry': 1639532929, 'httpOnly': False, 'name': 'csm-hit', 'path': '/',
             'secure': False, 'value': 'tb:s-Y26BW406MPTCXPD76RFP|1579052928522&t:1579052929166&adb:adblk_no'},
            {'domain': '.amazon.cn', 'expiry': 2209772928.051797, 'httpOnly': False, 'name': 'lc-acbcn', 'path': '/',
             'secure': False, 'value': 'zh_CN'}]
        self.max_num = 0
        # 【优先执行】
        # 1.打开选择导入表格
        self.get_path = requests_sides.file_path('get_price.xlsx')
        # print(get_path)
        # 2.读取配置信息
        self.get_data()

    def get_data(self):
        now_path_order = self.get_path
        input_info = input("是否隐藏运行：1，是；2，否")
        if str(input_info) == '2':
            visible_in = True
        else:
            visible_in = False
        app = wx.App(visible=visible_in, add_book=False)
        self.wb_info = app.books.open(now_path_order[0])
        print("导入数据...处理中...")
        """
        也可循环列表，来获取
        """
        # 【输出原信息列表】
        sheet_list = self.wb_info.sheets
        for sheet in sheet_list:
            # 配置信息
            rng_com_info = sheet.range(1, 1).expand().shape
            # print(common.cum_id[str(rng_com_info[1])])
            com_info_list = sheet.range(
                'A1' + ':' + common.cum_id[str(rng_com_info[1])] + str(rng_com_info[0])).value
            # print(com_info_list[0])
            self.initial_table.append(com_info_list)
        # # 品牌信息
        # # 参数配置
        # # 输出信息
        # 【输出匹配参数字典列表】
        # 1.需要匹配的字段
        self.match_field = [i[4] for i in self.initial_table[0] if i[4] is not None][1:]  # self.initial_table[0]配置信息
        # print(self.match_field)
        for k in self.match_field:
            # 2.字段所在位置
            index_field = self.initial_table[2][0].index(k)  # self.initial_table[2] 参数置配
            # print(k)
            # 3.生成字段的字典
            dic_field = {i[index_field + 1]: i[index_field] for i in self.initial_table[2] if
                         i[index_field] is not None}
            # print(dic_field)
            # 4.生成字典列表
            self.field_dic_list.append(dic_field)
        # 已购买记录信息
        self.bug_log_id = [i[1] for i in self.initial_table[6]]
        print(self.bug_log_id)
        # 已发送记录信息
        self.send_log_id = [i[0] for i in self.initial_table[6]]
        print(self.send_log_id)
        # 身份证信息dic
        self.id_number = {i[1]: i[2][-4:] for i in self.initial_table[8]}
        # print(self.id_number)
        self.id_number_list = [i[2] for i in self.initial_table[8]][1:]
        self.name_list = [i[1] for i in self.initial_table[8]][1:]
        # 初始 额度信息dic
        self.id_credit = {i[1]: int(i[4]) for i in self.initial_table[8][1:]}
        # print(self.id_credit)
        # 初始 通关信息dic
        self.id_name = {i[0]: i[5].split("|") for i in self.initial_table[7][1:]}
        # 是否隐藏运行
        self.hide_win = str(self.initial_table[0][15][5])
        # print(self.id_name)
        if self.hide_win == '是':
            self.wb_info.close()
            app.quit()
        # print(self.id_name['13580595590'])
        # print(self.field_dic_list)

    def limit_check(self):
        login_url = 'https://app.singlewindow.cn/ceb2pubweb/sw/personalAmount'
        # image_url = 'https://app.singlewindow.cn/ceb2pubweb/verifyCode/creator?timestamp='
        get_url = 'https://app.singlewindow.cn/ceb2pubweb/limit/outTotalAmount'
        headers = {
            "Referer": "https://app.singlewindow.cn/ceb2pubweb/sw/personalAmount",
            "Origin": "https://app.singlewindow.cn",
            "Host": "app.singlewindow.cn",
            # "Cookie": "JSESSIONID=0fddcefd-6dc0-4204-8886-af6a7cf00e34",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,zh-TW;q=0.6",
            # "Content-Length": "785",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
            # 0.获取列表
        session = requests.Session()
        session.get(url=login_url, headers=headers)
        # cookies = request.cookies.get_dict()
        for j, num_id in enumerate(self.id_number_list):
            # 加密身份证
            str_en = base64.b64encode(num_id.encode('utf-8'))
            num_id_ma = str_en.decode("utf-8")
            print(self.name_list[j])
            # print(num_id_ma)
            # 1.进入主页，获取验证码 打开 关闭 input
            # 验证码请求
            while True:
                timestamp = int(round(time.time() * 1000))
                # print(timestamp)
                image_url = 'https://app.singlewindow.cn/ceb2pubweb/verifyCode/creator?timestamp=' + str(timestamp)
                code_resp = session.get(image_url, headers=headers)
                with open(r'_tmp\code_resp.png', "wb") as f:
                    f.write(code_resp.content)
                time.sleep(1)
                # 展示图片e7458ad22ddbb76aa048ed4161768c6ae3e4bcf771ca422f9536fcc7fa1c69ec114121f8244d110e5aa8e8d5260fd58b
                images = Image.open(r'_tmp\code_resp.png')
                images.show()
                # 手动输入结果
                info_input = input('输入验证码：')
                # 2.发送请求,获取返回结果
                post_data = 'verifyCode='+ info_input +'&personalName=cXE%3D&idNumber='+ num_id_ma +'&sessionKey=verifyCode&queryCodeHidden=cebpub'
                print(post_data)
                rt = session.post(get_url, data=post_data, headers=headers)
                # print(rt.content.decode())
                text_dic = json.loads(rt.content.decode())
                # print(text_dic)
                # 判断获取结果：
                code = text_dic['code']
                if code =='40001':
                    print('验证码输入错误')
                    self.wb_info.sheets[8].range('E' + str(2 + j)).value = '验证码输入错误'
                else:
                    innerbalance = text_dic['result']['innerbalance']
                    print(innerbalance)
                    # 3.更新写入excel淦春
                    self.wb_info.sheets[8].range('E' + str(2 + j)).value = innerbalance
                    break

    # noinspection SpellCheckingInspection
    def crawl_data(self):  # 获取数据
        # 获取总数
        self.total_num = int(self.initial_table[0][3][5])
        # 每次获取个数
        self.get_num = int(self.initial_table[0][5][5])
        # 开始序列
        offset = 0
        # 是否只获取时实
        real_time = False
        if self.initial_table[0][1][5] == '实时监控':
            # print(self.initial_table[0][1][5])
            real_time = True
        if real_time:
            self.get_num = self.total_num = 15
        # 计算需要获取的次数
        count_get = int(self.total_num / self.get_num)
        # 设置headers
        headers = {
            "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            "Referer": "https://m.smzdm.com/ge/fenlei/437/?send_by=7005510644",
            "Host": "m.smzdm.com",
            "Connection": "keep-alive",
            'Accept-Encoding': 'gzip, deflate, br',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/plain, */*"}
        # 西部数据专项

        for index in range(count_get):
            wd_url = 'https://m.smzdm.com/ge/ajax_get_common_list?params=%7B%22common_type%22:1%7D&tab_params=%7B%22tab%22:%22haojia%22,%22channel%22:%22haojia%22,%22keyword%22:%22Western+Digital%5C%2F%5Cu897f%5Cu90e8%5Cu6570%5Cu636e%22,%22keyword_type%22:%22brand%22%7D&tag_params=&filter_params=%7B%22filter%22:%22faxian%22%7D&tab_ids=&limit=' + str(
                self.get_num) + '&time_sort=&offset=' + str(offset + self.get_num * index)
            request = requests.get(url=wd_url, headers=headers)
            son_dic = json.loads(request.text)
            # print(son_dic)
            data_empty = son_dic['error_msg']
            if data_empty == '数据为空':
                # 【容易出错地方】
                common.errorbox("返回数据为：%s ,退出" % data_empty)
                sys.exit()
            self.data_dic = son_dic['data']
            # print(len(self.data_dic))
            # print(self.data_dic)
            # 执行数据分析
            self.data_analysis()
        print('上次刷新时间:%s' % common.now_time('%Y-%m-%d %T'))

    # noinspection PyBroadException
    def data_analysis(self):
        # 数据清洗
        # print('获取。。。。。')
        # 获取输出信息，当前使用的列数
        output_use = 1
        if self.hide_win == '否':
            output_use = int(self.wb_info.sheets[3].range(1, 1).expand().shape[0])
        # print("当前处理第：%s 个，录入中..." % output_use)
        info_list_total = []
        send_value_list = []
        for i, k in enumerate(self.data_dic):
            tax = ''
            # print('第：%s 个 ' % (i + 1 + self.get_num * index))
            # 标题
            data_article_title = k['article_title']
            # print(data_article_title)
            # 价格
            data_article_price = k['article_price']
            # print(data_article_price)
            # 来源
            data_article_mall = k['article_mall']
            # print(data_article_mall)
            # 评价
            data_tongji_hudong = k['tongji_hudong']
            # print(data_tongji_hudong)
            # 上传人
            data_article_referrals = k['article_referrals']
            # print(data_article_referrals)
            # id
            data_article_id = k['article_id']
            # print(data_article_id)
            #  日期时间
            data_article_date = k['article_date']
            # print(data_article_date)
            # print("=" * 40)

            # 1. 获取输出的字段
            if self.initial_table[3][0] == '序号':
                output_info_field = self.initial_table[3]
            else:
                output_info_field = self.initial_table[3][0]
            # print('输出字段表：%s' % output_info_field)
            # 2. 循环匹配字段的处理方法
            info_list = []
            for o, field in enumerate(output_info_field):
                # 1.是否在关键字段列表
                field_value = None
                if field in self.match_field:
                    # print('是关键字段')
                    # 关键字，在模板的位置
                    index_fields = self.match_field.index(field)
                    # print(index_fields)
                    # 关键字对应的字典
                    field_dic = self.field_dic_list[index_fields]
                    # print(field_dic)
                    # 2.在.找到key列表
                    field_dic_keys = field_dic.keys()
                    # print(field_dic_keys)
                    # 列表 遍历是否包含在title里
                    for j in field_dic_keys:
                        # 在，字典匹配当前值 -》 不在，还回None
                        if j.upper() in data_article_title.upper():
                            # print(j)
                            field_value = field_dic[j]
                            break
                    # print(field_value)
                else:
                    # print('非关键字段')
                    # 3.不在按不同的属性 -序号  价格 来源 评价值否 上传人 id 日期时间

                    if field == "序号":
                        field_value = i + output_use
                    # 4.输出数据【的合并处理】
                    elif field == "输出数据":
                        field_value_temp = info_list[1:]
                        # 清理None
                        while True:
                            if None not in field_value_temp:
                                break
                            else:
                                # print('清理None')
                                field_value_temp.remove(None)
                        # print(field_value_temp)
                        # field_value_temp_2 = ' '.join(field_value_temp)
                        # print(field_value_temp_2)
                        # print(info_list)
                        field_value = str(info_list[0]) + "," + ' '.join(field_value_temp)
                    elif field == "原标题":
                        field_value = data_article_title
                    elif field == "价格":
                        # 价格处理优化
                        # 过期、卖完、用券、包邮，包税标识
                        # 未含税自动加税
                        # 美元转人民币
                        # 真实价（国内包邮价，海淘含税价）
                        # bug价判断
                        # 自动锁单功能【后继】
                        field_value = data_article_price
                    elif field == "到手价格":
                        # 1.判断是不否美元
                        dollar_f = False
                        dollar_list = ['美元', '$']
                        for dollar in dollar_list:
                            if dollar in data_article_price:
                                dollar_f = True
                                break
                        if dollar_f:
                            # print('美元商品')
                            # 分列 约 、 元 去￥
                            field_value = data_article_price.split('约')[1].split('元')[0].replace('￥', '').replace('¥',
                                                                                                                  '')
                        else:
                            field_value = data_article_price
                            if '元' in field_value:
                                field_value = field_value.split('元')[0]
                            if ' | ' in field_value:
                                field_value = field_value.split(' | ')[1]
                            field_value = field_value.replace('￥', '').replace('¥', '').replace('约', '')
                            # 如果未包邮或包税
                            if data_article_mall == '亚马逊海外购' and '税' not in data_article_price:
                                tax = 'no_tax'
                                # try:
                                #     # field_value = str(int(float(field_value) + float(field_value) * 0.091))
                                # except:
                                #     pass
                        # 2.非美完的处理
                    elif field == "备注":
                        remark_list = []
                        price_field_list = ['售罄', '过期', '$', '美元', '含税', '包邮', '直邮', '（需用券）']
                        price_field_list_t = ['售罄', '过期', '美元', '美元', '含税', '包邮', '直邮', '（需用券）']
                        for p, price_field in enumerate(price_field_list):
                            if price_field in data_article_price:
                                remark_list.append(price_field_list_t[p])
                        if len(remark_list) > 0:
                            field_value = '|'.join(remark_list)
                    elif field == "日期":
                        field_value = data_article_date
                    elif field == "评价数|值数":
                        field_value = data_tongji_hudong
                    elif field == "评价数":
                        # field_value = data_tongji_hudong
                        field_value = data_tongji_hudong.split(',')[0].split('_')[1]
                    elif field == "值数":
                        field_value_1 = int(data_tongji_hudong.split(',')[2].split('_')[1])
                        field_value_2 = int(data_tongji_hudong.split(',')[3].split('_')[1])
                        if field_value_2 + field_value_1 == 0:
                            field_value = 0
                        else:
                            field_value = "{:.2%}".format(field_value_1 / (field_value_1 + field_value_2))
                    elif field == "商品id":
                        field_value = data_article_id
                    elif field == "上传人":
                        field_value = data_article_referrals
                    elif field == "来源":
                        field_value = data_article_mall
                    # 5.是否值得买的【分析预警】
                    elif field == "购买建议":
                        # field_value = "暂不提供"
                        monitory_list = self.initial_table[1]
                        # 匹配大小、品牌
                        wd = info_list[1]
                        size_tb = info_list[7]
                        # print(size_tb)
                        brand = info_list[2]
                        # print(brand)
                        # 1. 机器 所有 每T 小于100 bug价
                        # price_win = 0
                        brand_price = [i for i in monitory_list if i[7] == size_tb and i[3] == brand]
                        # print(brand_price)
                        if len(brand_price) == 1:
                            price_win = brand_price[0][8]
                            try:
                                you_win = str(float(brand_price[0][10]) - float(info_list[12])).split(".")[0]
                                # print(you_win)
                                # print(type(you_win))
                                # sys.exit()

                                # print(good_info)
                                # 率
                                you_win_true = float(you_win) - 15
                                you_win_l = (float(you_win) - 15) / float(info_list[12])

                                good_info = "|".join([wd, brand, size_tb, "现", info_list[12]]) + "|推" + str(
                                    int(price_win)) + "|利" + str(you_win_true) + tax
                                # profits ='{:.2%}'.format(you_win_l)
                                # print(profits)
                                # if you_win_l>=0.04:
                                #     print("好收")
                                if int(price_win) >= float(info_list[12]) or you_win_l >= 0.04 or you_win_true > 50:
                                    # print('达到购买值可以推送')
                                    field_value = '【买】购买提醒->|' + str(good_info)
                                    # send_value = field_value
                                    send_value_list.append([data_article_id, good_info])
                                else:
                                    field_value = "【不】推荐购买->" + str(good_info)
                                    # send_value_list.append([data_article_id, good_info])
                                if float(you_win_true) > 0:
                                    print("[大妈利]：%s" % field_value)
                            except:
                                field_value = '未获取到建议'
                        else:
                            field_value = "【非】推荐产品"
                        # 1. 不同品牌不同价的
                        # 1. 一般值3%~5% 40 70 比较值5%~10%  非常值 250> 10%
                    else:
                        # print('未录入，字段...')
                        pass
                # print(field_value)
                # 3. 添加入，列表
                info_list.append(field_value)
            # print(info_list)
            info_list_total.append(info_list)
            # 4. 字段处理完成，写入excel
        if self.hide_win == '否':
            if self.initial_table[0][1][5] == '实时监控':
                # 实时清理旧的
                self.wb_info.sheets[4].range('A' + str(1 + output_use)).clear_contents()
                # 录入新的
                self.wb_info.sheets[4].range('A2').value = info_list_total
            else:
                self.wb_info.sheets[3].range('A' + str(1 + output_use)).value = info_list_total
        # print('总列表写入完成')
        # 推送处理：
        send_value_list = [i for i in send_value_list if str(i[0]) not in self.send_log_id]
        if self.initial_table[0][1][5] == '实时监控' and len(send_value_list) > 0:
            # 判断id 是否在 save 内
            for i in send_value_list:
                if i[0] not in self.send_value_save_id:
                    send_info = i[1] + "，" + common.now_time('%H%M')
                    # 发邮件
                    common.send_mail_tmp("13580595590@139.com", '13580595590@139.com', 'Qazqaz123', i[1])
                    # 发微信
                    self.server_sa('妈，' + send_info)
                    # 发短信
                    print('需发送:【大妈利提醒】：%s' % i[1])
                    # 记录已发送_id
                    self.send_value_save_id.append(i[0])
                else:
                    # print('已派发，暂不用处理')
                    pass

    def hdr_cart(self):
        # 1.获取更新价格
        # 打开
        driver = self.open_mark(self.cookies_oj, True)
        # 进入
        try:
            pass
            self.into_mark(driver)
            # 获取
            self.get_mark(driver)
            # 2.写入对比价格，对比出价格
            self.cart_analysis()
        except Exception as info:
            print('未知错误 %s' % info)
            self.server_sa('大哥，快去看看服务器挂啦~~' + common.now_time('%H%M'))
            # driver.quit()
            # self.driver_tb.quit()
            # sys.exit()
        # 3.提交购买锁单
        # 4.写入更新提交
        # 退出
        time.sleep(1)
        driver.quit()

    def cart_analysis(self):
        # 数据清洗
        # 获取输出信息，当前使用的列数
        # output_use = 1
        if self.initial_table[0][1][5] == '实时监控' and self.hide_win == '否':
            output_use = int(self.wb_info.sheets[5].range(1, 1).expand().shape[0])
            # 实时清理旧的
            self.wb_info.sheets[5].range('A' + str(1 + output_use)).clear_contents()
        # print("当前处理第：%s 个，录入中..." % output_use)
        info_list_total = []
        send_value_list = []
        # you_win_list = []
        for i, k in enumerate(self.mark_info[0]):
            # 标题
            data_article_title = k
            # print(data_article_title)
            # 价格
            data_article_price = self.mark_info[1][i]
            # print(data_article_price)
            # ID来源
            data_article_id = self.mark_info[2][i]
            # print(data_article_mall)
            # 1. 获取输出的字段
            if self.initial_table[5][0] == '序号':
                output_info_field = self.initial_table[5]
            else:
                output_info_field = self.initial_table[5][0]
            # print('输出字段表：%s' % output_info_field)
            # 2. 循环匹配字段的处理方法
            info_list = []
            for o, field in enumerate(output_info_field):
                # 1.是否在关键字段列表
                field_value = "未知"
                if field in self.match_field:
                    # print('是关键字段')
                    # 关键字，在模板的位置
                    index_fields = self.match_field.index(field)
                    # print(index_fields)
                    # 关键字对应的字典
                    field_dic = self.field_dic_list[index_fields]
                    # print(field_dic)
                    # 2.在.找到key列表
                    field_dic_keys = field_dic.keys()
                    # print(field_dic_keys)
                    # 列表 遍历是否包含在title里
                    for j in field_dic_keys:
                        # 在，字典匹配当前值 -》 不在，还回None
                        if j.upper() in data_article_title.upper():
                            # print(j)
                            field_value = field_dic[j]
                            break
                    # print(field_value)
                else:
                    if field == "序号":
                        field_value = i
                    # 4.输出数据【的合并处理】
                    elif field == "输出数据":
                        field_value_temp = info_list[1:]
                        # 清理None
                        while True:
                            if None not in field_value_temp:
                                break
                            else:
                                # print('清理None')
                                field_value_temp.remove(None)
                        field_value = str(info_list[0]) + "," + ' '.join(field_value_temp)
                    elif field == "原标题":
                        field_value = data_article_title
                    elif field == "价格":
                        field_value = data_article_price
                    elif field == "到手价格":
                        # 1.判断是否无货
                        data_article_price = data_article_price.replace('￥ ', "").replace(',', "").replace('。', "")
                        if '无货' in data_article_price or '内置硬盘' in data_article_price:
                            field_value = 50000
                        elif '从' in data_article_price:
                            data_article_price = re.findall(r"从 (.+) 元", data_article_price)[0]
                            field_value = "{:.2f}".format(float(data_article_price) * 1.091)
                        else:
                            field_value = "{:.2f}".format(float(data_article_price) * 1.091)
                        # 2.非美完的处理
                    elif field in ["备注", "日期", "评价数|值数", "评价数", "值数", "上传人", "备注"]:
                        field_value = None
                    elif field == "商品id":
                        field_value = data_article_id
                    elif field == "来源":
                        field_value = '购物车'
                    # 5.是否值得买的【分析预警】
                    elif field == "购买建议":
                        # field_value = "暂不提供"
                        monitory_list = self.initial_table[1]
                        # 匹配大小、品牌
                        wd = info_list[1]
                        size_tb = info_list[7]
                        brand = info_list[2]
                        # 1. 机器 所有 每T 小于100 bug价
                        # price_win = 0
                        brand_price = [i for i in monitory_list if i[7] == size_tb and i[3] == brand and i[1] == wd]
                        # 提前批

                        if len(brand_price) == 1:
                            price_win = brand_price[0][8]
                            # try:
                            you_win = str(float(brand_price[0][10]) - float(info_list[12])).split(".")[0]
                            # print(you_win)
                            # print(type(you_win))
                            # print(str(info_list[12]))
                            # sys.exit()
                            # good_info = "|".join([wd, brand, size_tb, "现", str(info_list[12])])

                            # print(good_info)
                            # 率
                            you_win_true = float(you_win) - 15
                            you_win_l = (float(you_win) - 15) / float(info_list[12])
                            # profits ='{:.2%}'.format(you_win_l)
                            good_info = "|".join([wd, brand, size_tb, "现", str(info_list[12])]) + "|推" + str(
                                int(price_win)) + "|利" + str(you_win_true)
                            # print(profits)
                            #     print("好收")
                            # 提醒列表
                            if int(price_win) >= float(info_list[12]) or you_win_l >= 0.065 or you_win_true > 100:
                                # print('达到购买值可以推送')
                                field_value = '【买】购买下单->' + str(good_info)
                                # send_value = field_value
                                send_value_list.append([data_article_id, good_info])
                            elif int(price_win) >= float(info_list[12]) or you_win_l >= 0.04 or you_win_true > 50:
                                # print('达到购买值可以推送')
                                field_value = '【买】购买提醒->' + str(good_info)
                                # send_value = field_value
                                send_value_list.append([data_article_id, good_info])
                            else:
                                field_value = "【不】推荐购买->" + str(good_info)
                                # send_value_list.append([data_article_id, good_info])
                            # 下单列表
                            if float(you_win_true) > 0:
                                print("[购物利]：%s" % field_value)
                            # except:
                            #     field_value = '未获取到建议'
                        else:
                            # print(brand)
                            # print(size_tb)
                            # print(wd)
                            # print(brand_price)
                            field_value = "【非】推荐产品"
                        # 1. 不同品牌不同价的
                        # 1. 一般值3%~5% 40 70 比较值5%~10%  非常值 250> 10%

                    else:
                        # print('未录入，字段...')
                        pass
                # print(field_value)
                # 3. 添加入，列表
                info_list.append(field_value)
            # print(info_list)
            info_list_total.append(info_list)
            # 4. 字段处理完成，写入excel
        if self.initial_table[0][1][5] == '实时监控' and self.hide_win == '否':
            # 实时清理旧的
            # self.wb_info.sheets[5].range('A' + str(1 + output_use)).clear_contents()
            # 录入新的
            self.wb_info.sheets[5].range('A2').value = info_list_total
        else:
            # 写入log
            date_ok = common.now_time('%m%d%H%M')
            with open(r"D:\FTP\bug_good_log\\" + "bug_good_log" + "" + date_ok + '.csv', 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for i in info_list_total:
                    # print(str_into)
                    writer.writerow(i)
        # print('总列表写入完成')

        # 推送处理：
        # 推送前的筛选
        send_value_list = [i for i in send_value_list if str(i[0]) not in self.send_log_id]

        if self.initial_table[0][1][5] == '实时监控' and len(send_value_list) > 0:
            # 判断id 是否在 save 内
            for i in send_value_list:
                if i[0] not in self.send_value_save_id:
                    send_info = i[1] + "，" + common.now_time('%H%M')
                    # 发邮件
                    # common.send_mail_tmp("13580595590@139.com", '13580595590@139.com', 'Qazqaz123', i[1])
                    # 发微信
                    # self.server_sa('购，' + send_info)
                    # 发短信
                    print('需发送:【购物车提醒】：%s' % i[1])
                    # 记录已发送_id
                    self.send_value_save_id.append(i[0])
                else:
                    # print('已派发，暂不用处理')
                    pass
        # 购买判断
        self.buy_goods(info_list_total)
        # 购买记录更新

        # 写入列表

    def buy_goods(self, info_list_total):
        # 获取购买帐号列表
        bug_account_list = [i for i in self.initial_table[7] if '是' in i[4]]
        # print(bug_account_list)
        # 获取购买产品列表
        bug_goods_list = [i for i in info_list_total if '下单' in i[21] and i[18] not in self.bug_log_id]
        # print(bug_goods_list)
        # print(len(bug_goods_list))
        if len(bug_goods_list) > 0:
            for ik, account in enumerate(bug_account_list):
                # 进入到购买
                # 配置 cookies 帐号 密码 通信信息额度
                # print(account)
                # cookies_tb = eval(account[7])
                # print(cookies_tb[1])
                # 打开新建浏览器
                self.driver_tb = self.open_mark(cookies_oj=None, open_tem=None)
                # 商品购买
                for i, bug_good in enumerate(bug_goods_list):
                    # 【获取购买次数，和每次个数,购买总数】
                    # 商品价
                    old_price = "{:.2f}".format(float(bug_good[11].replace('￥ ', "").replace(',', "")))
                    print("记录价格：%s" % old_price)
                    # 每次个数
                    every_one = int(5000 / float(old_price))
                    print("每次个数：%s" % every_one)
                    get_max = 10
                    if every_one > get_max:
                        every_one = get_max
                        # self.max_num = 8
                    print("真#每次个数：%s" % every_one)
                    # 购买链接：
                    bug_link = 'https://www.amazon.cn/gp/aw/d/' + bug_good[18]
                    ret = self.bug_face(self.driver_tb, bug_link, old_price, every_one, account)
                    if ret == '不可用帐号' or ret == '帐号地址无':
                        break
                self.driver_tb.quit()
            # 更新列表
            for l in bug_goods_list:
                self.bug_log_id.append(l[18])
            print('【购买提醒】购买商品已完成:%s' % common.now_time('%m-%d %T'))
        else:
            print('【购买提醒】未发现需购买商品:%s' % common.now_time('%m-%d %T'))

    def bug_face(self, driver, link, old_price, every_one, account):
        use_num = 0
        times = 0
        yu_num = 0
        every_one_true = every_one
        # 帐号登录
        login_url = 'https://www.amazon.cn/ap/signin?_encoding=UTF8&openid.assoc_handle=anywhere_v2_cn&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.cn%2F%3Fie%3DUTF8%26ref_%3Dnavm_hdr_signin'
        """
        //input[@id='ap_email_login']
        //span[@id='continue']//input[@id='continue']
        -----
        //input[@id='ap_password']
        //input[@id='signInSubmit']
        """
        driver.get(login_url)
        time.sleep(0.5)
        driver.implicitly_wait(15)
        driver.find_element_by_id("ap_email_login").clear()
        driver.find_element_by_id("ap_email_login").send_keys(account[0])
        time.sleep(0.5)
        driver.implicitly_wait(15)
        driver.find_element_by_xpath("//span[@id='continue']//input[@id='continue']").click()
        time.sleep(0.5)
        driver.implicitly_wait(15)
        driver.find_element_by_id("ap_password").clear()
        driver.find_element_by_id("ap_password").send_keys(account[1])
        time.sleep(0.5)
        driver.implicitly_wait(15)
        time.sleep(0.5)
        driver.implicitly_wait(15)
        driver.find_element_by_xpath("//input[@id='signInSubmit']").click()
        while True:
            driver.get(link)
            # 价格匹配
            time.sleep(1)
            driver.implicitly_wait(30)
            now_price_tmp = driver.find_element_by_xpath("//span[@id='priceblock_ourprice']").text
            now_price = "{:.2f}".format(float(now_price_tmp.replace('￥', "").replace(',', "").replace(' ', "")))
            print("真实价格：%s" % now_price)
            if float(old_price) + 2 >= float(now_price):
                print("价格匹配")
            # 初次设置购买个数
            # 打开选项 //span[@id='a-autoid-0-announce']
            time.sleep(1.5)
            driver.implicitly_wait(30)
            driver.find_element_by_xpath("//span[@id='a-autoid-0-announce']").click()
            driver.implicitly_wait(30)
            time.sleep(1.5)
            # 选项列表 /html[1]/body[1]/div[7]/div[1]/div[2]/ul[1]//a[1]
            option_list = driver.find_elements_by_xpath('/html[1]/body[1]//div[1]/div[2]/ul[1]//a[1]')
            # 判断 可先个数
            # 总数 每次最多的数 次数
            if use_num == 0:
                self.max_num = len(option_list)
                # self.max_num = 2
                if self.max_num > 9:
                    self.max_num = 10
                    # self.max_num = 3
                if self.max_num <= every_one:
                    every_one_true = self.max_num
                #  每次最多的数 every_one
                # 余数
                yu_num = int(self.max_num) % int(every_one_true)
                #  次数
                if int(self.max_num) % int(every_one_true) == 0:
                    times = int(int(self.max_num) / int(every_one_true))
                else:
                    times = int(int(int(self.max_num) / int(every_one_true)) + 1)
                print("总数：%s每次数：%s次数：%s" % (self.max_num, every_one_true, times))
                # 选 点击
            # 当最后次数，且余数大于0，当前个数选 ->余数
            use_num += 1
            if yu_num > 0 and use_num == times:
                every_one_true = yu_num
            option_list[(every_one_true - 1)].click()

            # 加入购物车
            time.sleep(1)
            js = "var q=document.documentElement.scrollTop=240"
            driver.execute_script(js)
            time.sleep(2)
            driver.implicitly_wait(30)
            # driver.find_element_by_xpath("//input[@id='buy-now-button']").click()  //button[@id='add-to-cart-button']
            # driver.find_element_by_xpath("//input[@id='add-to-cart-button']").click()
            # /html[1]/body[1]/div[1]//div[1]//form[1]/div[1]/span[1]/span[1]/span[1]
            # driver.find_element_by_xpath("//span//div[@class='displayAddressDiv']").click()
            driver.find_element_by_xpath(
                "/html[1]/body[1]/div[1]//div[1]//form[1]/div[1]/span[1]/span[1]/input[1]").click()
            time.sleep(3)
            print('加入购物车')
            # 进入结算中心
            driver.implicitly_wait(30)
            # driver.find_element_by_xpath("//input[@id='buy-now-button']").click()
            driver.find_element_by_xpath("//button[@id='a-autoid-0-announce']").click()
            time.sleep(2)
            # sys.exit()

            """
            # 判断身份证信息是否正确
            # 判断购买人的额度是否满足，不满足
            # 选择正确信息 /html[1]/body[1]/div[6]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[1]//div[1]/span[1]/div[1]/label[1]/span[1]/div[1]/ul[1]/li[1]/b[1]
            # 设为默认信息
            # 额度判断更新额度
            """
            # 获取当前帐号 购买人列表
            goods_ren_list = self.id_name[account[0]]
            print("购买人列表：%s" % goods_ren_list)
            name_user_x = driver.find_element_by_xpath(
                "//div[@id='shipping-summary']//li[@class='displayAddressLI displayAddressFullName']")
            name_user = name_user_x.text
            name_user_text_x = driver.find_element_by_xpath(
                "/html[1]/body[1]//div[1]/div[1]/div[1]/form[1]/div[1]/div[7]/div[1]/a[2]/div[1]/span[1]")
            name_user_text = name_user_text_x.text
            name_user_id = name_user_text[7:11]
            name_user_m = False
            name_user_id_m = False
            print("默认的购买人：%s；id：%s" % (name_user, name_user_id))
            # 商品消耗额度
            credit_out = float(now_price) * int(every_one_true)
            # 默认的购买人额度
            credit_all = float(self.id_credit[name_user])
            print(credit_all)
            # 使用后额度
            credit_update = credit_all - credit_out
            # 如果默认可用
            if name_user == goods_ren_list[0] and credit_update > 0:
                name_user_m = True
                name_user_true = name_user
                name_user_id_true = self.id_number[name_user_true]
            else:
                name_user_true = ''
                name_user_id_true = ''
                if name_user in goods_ren_list:
                    # 重设置可用列表
                    goods_ren_list.remove(name_user)
                    self.id_name[account[0]] = goods_ren_list
                # 找一个可以用的额度的
                for ig in goods_ren_list:
                    # 更新后购买人额度
                    print(ig)
                    credit_all = float(self.id_credit[ig])
                    print(credit_all)
                    # 使用后额度
                    credit_update = credit_all - credit_out
                    if credit_update > 0:
                        name_user_true = ig
                        name_user_id_true = self.id_number[name_user_true]
                        break
                    else:
                        # 更新可购买人
                        goods_ren_list.remove(ig)
                        self.id_name[account[0]] = goods_ren_list
            # 确定身份id self.id_number
            credit_update = "{:.2f}".format(float(credit_update))
            print("确认购买人：%s；id：%s；用后额度：%s" % (name_user_true, name_user_id_true, credit_update))
            if len(goods_ren_list) < 1:
                print("当前帐号无可用额度")
                return "不可用帐号"
            # 更新额度
            self.id_credit[name_user_true] = credit_update
            # //span//li[@class='displayAddressLI displayAddressFullName']
            # /html[1]/body[1]/div[6]/div[1]/div[1]/div[1]/form[1]/div[1]/div[7]/div[1]/a[2]/div[1]/span[1]
            # 选择购买人：
            if not name_user_m:
                time.sleep(3)
                driver.implicitly_wait(8)
                # //span//div[@class='displayAddressDiv']
                driver.find_element_by_xpath("//span//div[@class='displayAddressDiv']").click()
                time.sleep(3)
                driver.implicitly_wait(8)
                # 选正确的帐号
                # 选择位置，确认位置
                name_add_list_x = driver.find_elements_by_xpath(
                    '/html[1]/body[1]//div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[1]//div[1]/span[1]/div[1]/label[1]/span[1]/div[1]/ul[1]/li[1]/b[1]')
                sure_list_x = driver.find_elements_by_xpath("//span/a[contains(text(),'送货到该地址')]")
                # /html[1]/body[1]/div[6]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[1]//div[1]/span[1]/div[1]/label[1]/span[1]/div[1]/ul[1]/li[1]/b[1]
                # //span/a[contains(text(),'送货到该地址')]
                name_add_list = [i.text for i in name_add_list_x]
                print(name_add_list)
                if name_user_true in name_add_list:
                    # 获取位置
                    index_name = name_add_list.index(name_user_true)
                    # 点击位置
                    name_add_list_x[index_name].click()
                    time.sleep(2)
                    driver.implicitly_wait(8)
                    sure_list_x[index_name].click()
                    # 送货方式
                    time.sleep(3)
                    driver.implicitly_wait(8)
                    try:
                        driver.find_element_by_xpath("//span[@id='a-autoid-0']//input[@class='a-button-input']").click()
                        # time.sleep(2)
                    except:
                        pass
                else:
                    print("当前帐号地址无")
                    return "帐号地址无"
            # 选择人id
            if name_user_id_true in name_user_id:
                name_user_id_m = True
            if not name_user_id_m:
                time.sleep(3)
                driver.implicitly_wait(8)
                # //a[@class='a-touch-link a-box a-last a-declarative']//div[@class='a-box-inner']/span[1]
                driver.find_element_by_xpath(
                    "//a[@class='a-touch-link a-box a-last a-declarative']//div[@class='a-box-inner']/span[1]").click()
                # //span[@class='a-dropdown-prompt']  进入
                time.sleep(3)
                driver.implicitly_wait(8)
                driver.find_element_by_xpath("//span[@class='a-dropdown-prompt']").click()
                time.sleep(3)
                driver.implicitly_wait(8)  # /html[1]/body[1]/div[12]/div[1]/div[2]/ul[1]/li/a[1]
                id_list_x = driver.find_elements_by_xpath("/html[1]/body[1]//div[1]/div[2]/ul[1]//a[1]")
                # print(id_list_x)
                id_list_test_x = [i.text for i in id_list_x]
                print('身份列表:%s' % id_list_test_x)
                # id 位置
                index_ids = None
                for ids, id_list in enumerate(id_list_test_x):
                    if name_user_true in id_list:
                        index_ids = ids
                        break
                if index_ids is None:
                    print("当前帐号身份无")
                    return "帐号地址无"
                id_list_x[index_ids].click()
                # /html[1]/body[1]/div[12]/div[1]/div[2]/ul[1]//a[1]  列表
                time.sleep(2)
                driver.implicitly_wait(8)
                driver.find_element_by_xpath("//input[@class='a-button-input']").click()
                # //input[@class='a-button-input']
                # 送货方式
                time.sleep(3)
                driver.implicitly_wait(8)
                try:
                    driver.find_element_by_xpath("//span[@id='a-autoid-0']//input[@class='a-button-input']").click()
                except:
                    pass
                # //span[@id='a-autoid-0']//input[@class='a-button-input']
            # 定单提交 //span[@id='placeYourOrder']//input[@name='placeYourOrder1']
            time.sleep(1)
            driver.implicitly_wait(30)
            driver.find_element_by_xpath("//span[@id='placeYourOrder']//input[@name='placeYourOrder1']").click()
            # 判断身份证息信是否正确
            # 判断是否需要重复下单
            time.sleep(1)
            driver.implicitly_wait(8)
            try:
                driver.find_element_by_xpath("//input[@name='forcePlaceOrder']").click()
                time.sleep(2)
            except:
                pass
            # //input[@name='forcePlaceOrder']
            #  //input[@name='forcePlaceOrder']
            # 判断能购买的个数。 再判断需买买的次数
            # if use_num >= 2: break
            if use_num >= times:
                break

    def open_mark(self, cookies_oj=None, open_tem=None):
        options = Options()
        # open_tem = True
        # 【【【【获取cookies】】】
        get_cookies = 0
        if open_tem and get_cookies ==0:
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)

        mobile_emulation = {'deviceName': 'iPhone X'}
        options.add_experimental_option('mobileEmulation', mobile_emulation)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        if self.hide_win == '是':
            show_go = True
        else:
            show_go = False
        if show_go:
            options.add_argument('--disable-dev-shm-usage')
            # # options.add_argument('window-size=1366x768')
            options.add_argument('--disable-gpu')
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        # driver.add_cookie(cookie_dic)
        driver.get('https://www.amazon.cn/gp/aw/d/B07GP1GW25')

        if get_cookies ==1:
            while True:
                tb_cookies  = driver.get_cookies()
                print(tb_cookies)
                time.sleep(8)
        # return driver
        # 注入 cookies
        if cookies_oj is None:
            pass
        else:
            for cookie in cookies_oj:
                cookies = {"name": cookie['name'], "value": cookie['value']}
                driver.add_cookie(cookies)
        return driver

    @staticmethod
    def into_mark(driver):
        # driver.get('https://www.amazon.cn/gp/aw/d/B07VNTFHD5/ref=ox_sc_act_image_1?smid=A2EDK7H33M5FFG&psc=1')
        # 到收藏夹
        driver.get('https://www.amazon.cn/gp/aw/c/?ie=UTF8&ref_=navm_hdr_cart')
        # 获取收藏数
        # //h1[@class='sc-list-caption sc-java-remote-feature']
        my_data = driver.find_element_by_xpath("//h1[@class='sc-list-caption sc-java-remote-feature']").text
        # print(int(my_data[4:7]))
        num_go = int(int(my_data[4:7]) / 10) - 1
        # print(num_go)
        if float(int(my_data[4:7]) / 10) > float(int(int(my_data[4:7]) / 10)):
            num_go = num_go + 1
        print('正加载购物车数据数据...%s' % num_go)
        time.sleep(2)
        # print()
        for i in range(num_go):
            # print(i) # //button[@id='a-autoid-21-announce']
            # time.sleep(1)
            while True:
                try:
                    driver.implicitly_wait(30)
                    driver.find_element_by_xpath("//button[contains(text(),'显示更多')]").click()
                    break
                except:
                    # print("加载加时")
                    time.sleep(0.5)
            time.sleep(3)
        print("加载完成")

    def get_mark(self, driver):
        title_list = []
        price_list = []
        price_list_2 = []
        goods_id_list = []
        title_list_oj = driver.find_elements_by_xpath(
            '/html[1]/body[1]/div[1]/div[2]/div[1]//form[1]/div[1]//div[4]/div[1]/div[1]/div[1]/div[2]/span[1]')
        title_price_oj = driver.find_elements_by_xpath(
            '/html[1]/body[1]/div[1]/div[2]/div[1]//form[1]/div[1]//div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[1]/span[1]/span[1]')
        title_price_oj2 = driver.find_elements_by_xpath(
            '/html[1]/body[1]/div[1]/div[2]/div[1]//form[1]/div[1]//div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[2]/span[1]/span[1]')
        goods_id = driver.find_elements_by_xpath('/html[1]/body[1]/div[1]/div[2]/div[1]//form[1]/div[1]/div')
        # print(len(title_list_oj))
        # print(len(title_price_oj2))
        # /html[1]/body[1]/div[1]/div[2]/div[1]/div[6]/form[1]/div[1]//div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[1]/span[1]/span[1]
        # /html[1]/body[1]/div[1]/div[2]/div[1]/div[6]/form[1]/div[1]//div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[2]/span[1]/span[1]
        # /html[1]/body[1]/div[1]/div[2]/div[1]/div[6]/form[1]/div[1]//div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[1]/span[1]/span[1]/span[1]
        for i, title in enumerate(title_list_oj):
            title_list.append(title.text)
            price_list.append(title_price_oj[i].text)
            goods_id_list.append(goods_id[i].get_attribute('data-asin'))
        # print(title_list)
        # 价格整理
        # print(price_list)
        for i, prices in enumerate(title_price_oj2):
            price_list_2.append(prices.text)
        # print(price_list_2)
        price_list_2 = [i for i in price_list_2 if '￥' in i]
        # print(price_list_2)
        index_other = 0
        # print(price_list)
        for i, pri in enumerate(price_list):
            # print(pri)
            # print(index_other)
            if '￥' in pri or '无货' in pri:
                pass
            else:
                price_list[i] = price_list_2[index_other]
                index_other += 1
        # print(price_list)
        # print(goods_id_list)
        self.mark_info = [title_list, price_list, goods_id_list]

    @staticmethod
    def server_sa(send_info):
        url = 'https://sc.ftqq.com/SCU76380Tc062d606bf4c2b917b12653f6f5bf1135e13fa8e8edf4.send?text=' + send_info + '&desp=' + send_info
        requests.get(url)
        # print(req)

    @common.use_times
    def main(self):
        modes =0
        if modes == 1:
            self.limit_check()
        else:
            # sys.exit()
            # 3.爬取数据信息，分析数据
            print("当前没每隔:%s 分钟刷新一次" % int(self.initial_table[0][7][5]))
            if self.initial_table[0][3][6] == '是':
                self.crawl_data()
            if self.initial_table[0][1][6] == '是':
                self.hdr_cart()
            # 4.分析数据信息
            # 5.写入归档数据信息
            # 定时刷新
            if self.initial_table[0][1][5] == '实时监控':
                if self.initial_table[0][3][6] == '是':
                    minutes_time = int(self.initial_table[0][7][5])
                    # print(common.now_time('%Y%m%d %T'))
                    schedule.every(minutes_time).minutes.do(self.crawl_data)
                if self.initial_table[0][1][6] == '是':
                    minutes_time2 = int(self.initial_table[0][9][5])
                    schedule.every(minutes_time2).minutes.do(self.hdr_cart)
                while True:
                    schedule.run_pending()
                    time.sleep(2)


if __name__ == "__main__":
    # 启动获取
    price = GetPrice()
    price.main()
