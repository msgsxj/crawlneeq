# 爬取neeq.com.cn上数据
应正在实习的同学的需求爬取neep.com.cn上部分数据,好了话不多说直接上思路:
code分三步走:
 1. get data
 2. clean data
 3. save to excel

## get data
路线为F12分析得到request url,用python自带urllib模块得到json格式数据.获取数据的三个函数分别为gethomepagedata(),getstockdata(),getxyzrdata().
 - 其中getxyzrdata()涉及多页数据,故写入一个判断语句,如果当前页面返回的json数据的行末中匹配到了'"lastPage":true'则停止爬取.

## clean data
主要是用json模块的json.loads()函数将字符串化为json数据,然后提取需要数据.

## save to excel
路线为pandas模块的pd.ExcelWriter()函数,将DataFrame型数据用to_excel()函数写入sheet

# 修改
 - 2018/4/26 改用requests模块的get()方法
