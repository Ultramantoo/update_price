import base64

""""""

id_number = '441621198704053017'
str_en = base64.b64encode(id_number.encode('utf-8'))
print(str_en)
# 编码转换去（b'）
print(str_en.decode("utf-8"))



"""
0.获取列表
1.进入主页，获取验证码 打开 关闭 input
2.发送请求,获取返回结果
3.更新写入excel
"""


"""
https://app.singlewindow.cn/ceb2pubweb/verifyCode/creator
https://app.singlewindow.cn/ceb2pubweb/sw/personalAmount
https://app.singlewindow.cn/ceb2pubweb/limit/outTotalAmount
Request URL: 
Request Method: POST
Status Code: 200 OK

1585849083387
1585849772982
1585849588.2548118
"""

"""
verifyCode=w23a&personalName=cXE%3D&idNumber=NDQxNjIxMTk4NzA0MDUzMDE3&sessionKey=verifyCode&queryCodeHidden=cebpub
verifyCode=T4k9&personalName=cXE%3D&idNumber=NDQxNjIxMTk4NzA0MDUzMDE3&sessionKey=verifyCode&queryCodeHidden=cebpub

"""

"""
{code: "0", total: 0, serviceTime: 1585474158307,…}
code: "0"
total: 0
serviceTime: 1585474158307
result: {innerbalance: 15920.34, totalAmount: 10079.66}
innerbalance: 15920.34
totalAmount: 10079.66
operResult: false
authLegalCheck: true
success: true
"""