""""""

tt= '12345678'

tt2= tt[::2]

print(tt2)

sss = '001'
print(sss)
print(int(sss))
"""
进入亚马逊返利
1.进入  https://www.fanli.com/shop/amazonht
2.登录跳转 https://fun.fanli.com/goshop/go?id=1733&lc=shopdetail_goumai&sign=8b4fc758&v=1589533573050

--进入手机密码登录
选：//input[@id='J_login_radio1']
手机：//input[@id='J_login_user']   输入
密码：//div[@id='J_login']//input[1]   输入
点击登录 ：//a[@id='btn-login']


//a[@id='nav-logobar-greeting']

首页的 搜索框
//input[@id='nav-search-keywords']

//div[@class='nav-search-submit']//input[@class='nav-input']

允许购买个数

单次最大购买个数
"""
'''
进入到亚逊
登录：
//a[@id='nav-link-yourAccount']

//input[@id='ap_email']
//input[@id='ap_password']

//input[@id='signInSubmit']


搜索框 ：//input[@id='twotabsearchtextbox']
点击搜索//div[@class='nav-search-submit nav-sprite']//input[@class='nav-input']

获取标题列表：
/html[1]/body[1]//div[1]/span[4]/div[1]//div[1]//h2[1]/a[1]/span[1]
-------

获取价格列表：
/html[1]/body[1]//div[2]/div[1]/span[4]//span[1]/span[2]/span[2]
-----
点击进入

切换窗口

获取最低价： 点击  价格判断
//a[@class='a-link-normal']//span[@class='a-color-price']

加入购物车：
/html[1]/body[1]//div[4]//div[1]//div[5]/div[1]//span[1]/input[1]

进入结算中心：
//a[@id='hlb-ptc-btn-native']

/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/span[1]

/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]//div[1]/div[1]/span[1]

/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/span[1]

/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/form[1]/span[1]/span[1]/span[1]/input[1]
/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/form[1]/span[1]/span[1]/span[1]/input[1]
/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]//div[1]/div[2]/div[2]/div[1]/form[1]/span[1]/span[1]/span[1]/input[1]


# 额度查询
//input[@id='personalName']
//input[@id='idNumber']
//input[@id='inputCode']
//input[@id='searchButton']
//div[@id='surplus']

/html[1]/body[1]/div[1]/div[2]/div[1]/div[9]/form[1]/div[1]//div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[2]/span[1]/span[1]
/html[1]/body[1]/div[1]/div[2]/div[1]/div[9]/form[1]/div[1]//div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[1]/span[1]/span[1]

/html[1]/body[1]/div[1]//div[9]/div[8]//div[1]/table[1]/tbody[1]/tr[1]/td[2]/span[1]
/html[1]/body[1]/div[1]//div[9]/div[8]//div[1]/table[1]/tbody[1]/tr[1]/td[2]/span[1]

/html[1]/body[1]/div[1]/div[2]/div[1]/div[9]/form[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[2]/span[1]/span[1]/span[1]
/html[1]/body[1]/div[1]/div[2]/div[1]/div[9]/form[1]/div[1]/div[6]/div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[3]/span[1]/span[1]/span[1]



//span[@class='a-size-small a-color-price sc-product-availability']

//span[@class='a-size-small a-color-success sc-product-availability']
a-size-small a-color-success sc-product-availability

/html[1]/body[1]/div[1]/div[2]/div[1]/div[9]/form[1]/div[1]/div[46]/div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[2]/span[1]/span[1]/span[1]

# 状态
/html[1]/body[1]/div[1]/div[2]/div[1]//form[1]/div[1]//div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[1]/span[1]/span[1]
/html[1]/body[1]/div[1]/div[2]/div[1]/div[9]/form[1]/div[1]//div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[1]/span[1]/span[1]
# 价钱
//span[@class='a-size-base a-color-price sc-white-space-nowrap sc-product-price sc-price-sign']

/html[1]/body[1]/div[1]/div[2]/div[1]/div[9]/form[1]/div[1]/div[6]/div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[3]/span[1]/span[1]/span[1]
/html[1]/body[1]/div[1]/div[2]/div[1]/div[9]/form[1]/div[1]//div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[3]/span[1]/span[1]/span[1]


/html[1]/body[1]/div[1]/div[2]/div[1]/div[9]/form[1]/div[1]/div[5]/div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[2]/span[1]/span[1]/span[1]
/html[1]/body[1]/div[1]/div[2]/div[1]/div[9]/form[1]/div[1]/div[7]/div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[3]/span[1]/span[1]/span[1]
'''

'/html[1]/body[1]/div[1]/div[2]/div[1]//form[1]/div[1]/div[6]/div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[3]/span[1]/span[1]/span[1]'
'/html[1]/body[1]/div[1]/div[2]/div[1]//form[1]/div[1]/div[6]/div[4]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[1]/span[1]/span[1]'