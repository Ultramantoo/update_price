# -*- coding: utf-8 -*-
import common

import time
from os import path
import win32ui
import sys
import re

import requests
from PIL import Image
import pytesseract

city_id = {"广州": "86020",
           "韶关": "860751",
           "深圳": "860755",
           "珠海": "860756",
           "汕头": "860754",
           "佛山": "860757",
           "江门": "860750",
           "湛江": "860759",
           "茂名": "860668",
           "肇庆": "860758",
           "惠州": "860752",
           "梅州": "860753",
           "汕尾": "860660",
           "河源": "860762",
           "阳江": "860662",
           "清远": "860763",
           "东莞": "860769",
           "中山": "860760",
           "潮州": "860768",
           "揭阳": "860663",
           "云浮": "860766"}


# 可以汇聚1 [ # 导入，获得选取文件路径，我清除文件]
# 1.增加是否弹窗口[选择固定文件]
def file_path(info_path=None):
    # info_path = None
    common.deadline()
    # 创建文件获取路径
    common.mkdir("_tmp")
    common.del_dir(r"_tmp\tmp_text.txt")
    print("读取配置信息...")
    # 1表示打开文件对话框
    with open(r'_tmp\filepath.txt', 'w') as f:
        # print("写入")
        f.write('Hello, world!')
    # 1表示打开文件对话框
    file = path.abspath(r'_tmp\filepath.txt')
    # print(file)
    files = file.replace(r'filepath.txt', "")
    files_s = file.replace(r'_tmp\filepath.txt', "")
    # 注册码校准
    common.check_info()
    # print(files)
    # print(files_s)
    print("导入文件...请选择需要导入的文件")
    if info_path is None:
        dlg = win32ui.CreateFileDialog(1)
        dlg.SetOFNInitialDir(files_s)  # 设置打开文件对话框中的初始显示目录
        dlg.DoModal()
        filename = dlg.GetPathName()  # 获取选择的文件路径
    else:
        filename = files_s + info_path
    # print(filename)
    # 读取创建一个新的，并写入保存，关闭
    with open(r'_tmp\filepath.txt', 'w') as f:
        # print('正在写入')
        f.write(filename)
    print([filename, files_s, files])
    return [filename, files_s, files]


# 可以汇聚2 [ # 根据获取帐号对的信息（人名，和帐号库）]
def data_analyze(plan_one_list, accounts_list):
    # 使用帐号
    # print("# 使用帐号")
    use_accounts = plan_one_list
    # 和cookies分析
    username = password = cookies = use_times = ""
    # password = ""
    # use_time = ""
    # cookies = ""
    for use_index in range(1, len(accounts_list)):
        # print(use_accounts)
        # print(accounts_list[use_index][0])
        if use_accounts == accounts_list[use_index][0]:
            username = accounts_list[use_index][1]
            password = accounts_list[use_index][2]
            use_times = accounts_list[use_index][3]
            cookies = accounts_list[use_index][4]
            print("正处理帐号为：{}".format(use_accounts))
            break
    # print("返回分析")
    # use_time = ""
    if username == "":
        common.errorbox("【警告】获取帐号失败，请确认模板帐号信息！！")
        sys.exit()
    # print([username, password, use_time, cookies])
    return [username, password, use_times, cookies]
    # 是否续传[暂不续传]


# 可以汇聚3 [# 通过 帐号密码进行登录 返回值]
# noinspection PyBroadException,SpellCheckingInspection
def get_cookies(all_data):
    # 获取 cookies
    # print("开始登录...处理中...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        # "Referer": "https://nqi.gmcc.net:20443/ltemr-portal/modules/ltescheme/unify/disquery/showgis.jsp?timeStart=2019-01-01&timeEnd=2019-07-24&vccity=860752",
        "Origin": "https://nqi.gmcc.net:20443",
        "Host": "nqi.gmcc.net:20443",
        # "Content-Length": "785",
        "Connection": "keep-alive",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01"}
    username = all_data[0]
    username = common.encrpt(username)
    password = all_data[1]
    password = common.encrpt(password)
    # use_time = all_data[2]
    # cookies = all_data[3]
    login_url = "https://nqi.gmcc.net:20443/cas/login?service=http%3A%2F%2Fnqi.gmcc.net%3A8090%2Fpro-portal%2F"
    image_url = "https://nqi.gmcc.net:20443/cas/captcha.htm"
    goto_url = "https://nqi.gmcc.net:20443/ltemr-portal/portal?menuname=fagzt&address=/module/ltescheme/activity/lte_unify_activity.jsp?type=zd"
    login_num = 0
    while True:
        if login_num >= 3:
            print("登录失败次数：%s,请退出程序，核查帐号密码。" % login_num)
            time.sleep(5)
            # return False
        # url = "https://nqi.gmcc.net:20443/ltemr-portal/portal?menuname=jlwtd&address=/modules/ltescheme/unify/disquery/showgis.jsp?timeStart=2019-07-01%26timeEnd=2019-07-02%26vccity=860752"
        session = requests.Session()
        request = session.get(url=login_url, headers=headers)
        # print(request.status_code)  # 打印状态码
        cookies = request.cookies.get_dict()
        # print(json.dumps(cookies))
        str_html = request.text
        # 获取 execution Lt
        lt = re.findall(r"lt\" value=\"(.+)\" />", str_html)[0]
        # print(lt)
        execution = re.findall(r"execution\" value=\"(.+)\" />", str_html)[0]
        # print(execution)
        _eventId = "submit"
        # 【获取图片，保存】
        while True:
            code_resp = session.get(image_url, headers=headers, cookies=cookies)
            with open(r'_tmp\code.png', "wb") as f:
                f.write(code_resp.content)
            # 识别载图
            image = Image.open(r'_tmp\code.png')
            # 预处理载图
            image_in = common.convert_image(image)
            time.sleep(1)
            code = pytesseract.image_to_string(image_in).replace(" ", "")
            # print("初始验证码： %s" % code)
            try:
                code = int(code)
                break
            except:
                # print("验证验错误,重新获得取...")
                pass
        image_in.save(r'_tmp\code_tmp.png')
        code = common.encrpt(str(code))

        # 发送登录请求
        post_data = {"lt": lt,
                     "execution": execution,
                     "username": username,
                     "password": password,
                     "_eventId": "submit",
                     "j_captcha_response": code}
        # print(post_data)
        session.post(login_url, data=post_data, headers=headers, cookies=cookies)
        # print(r.status_code)  # 打印状态码
        # print(r.text)  #以文本形式打印网页源码
        # 跳转到方案页面
        rt = session.get(goto_url, headers=headers, cookies=cookies)
        # print(rt.status_code)  # 打印状态码
        # print(rt.url)          # 打印请求url
        # print(rt.text)  #以文本形式打印网页源码w
        cookies_now = rt.cookies.get_dict()
        cookies_now["JSESSIONID"] = cookies["JSESSIONID"]
        # print(len(cookies_now))
        if len(cookies_now) >= 3:
            # print("登录成功")
            break
        else:
            # print("登录失败, 重试处理中。。。")
            login_num += 1
            session.close()
            # print(cookies_now)
            # print(rt.text)  # 以文本形式打印网页源码w
            # common.errorbox("获取失败:[%s]，请重试。。。" % len(cookies_now))
            # sys.exit()
    return [cookies_now, headers, session]


# 可以汇聚4 队列临时写入
def write_list(q):
    # 读列队结果
    while not q.empty():
        str_data = q.get()
        # print(str_data)
        # 写入结果
        with open(r"_tmp\tmp_text.txt", "a+") as f:
            f.write(str_data + "\n")
