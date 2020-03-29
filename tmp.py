import base64

""""""

"""
0.获取列表
1.进入主页，获取验证码 打开 关闭 input
2.发送请求,获取返回结果
3.更新写入excel
"""

"""
Request URL: https://app.singlewindow.cn/ceb2pubweb/limit/outTotalAmount
Request Method: POST
Status Code: 200 OK
"""

"""
verifyCode=w23a&personalName=cXE%3D&idNumber=NDQxNjIxMTk4NzA0MDUzMDE3&sessionKey=verifyCode&queryCodeHidden=cebpub
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