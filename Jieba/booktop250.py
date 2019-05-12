#通过requests库和BeautifulSoup库来实现内容的获取和解析
import requests
from bs4 import BeautifulSoup
import re
import pandas
#jieba分词+词云
import jieba
#文件输入输出包
from os import path
#图片读取包
from scipy.misc import imread
#画图包
import matplotlib.pyplot as plt
#词云包
from wordcloud import WordCloud,ImageColorGenerator
#获取解析内容
dict1=[]
dict=[]
for num in range(10):
    url='https://book.douban.com/top250?start='+ str(num*25)
    r=requests.get(url)
    #print(r.status_code)
    html=r.text
    soup=BeautifulSoup(html,'html.parser')

    #select方法：标签名不动，类名加点号，ID加#组合查找中间用空格隔开
    items=soup.select('.item')
    for item in items:
        bookName=item.select('a')[1].text.strip()
        #获取详情栏信息
        infor=item.select('p')[0].text
        price=infor.split('/')[-1]
        time=infor.split('/')[-2]
        store=infor.split('/')[-3]
        autor=infor.split('/')[0]
        score=item.select('.rating_nums')[0].text
        #输出文件时发现，评价数在Excel格式不能正常显示，查看页面发现是评价数前面有（）
        #先切掉括号，在去掉空格，这里暂时没找到更好的办法
        pjNum = item.select('.pl')[1].text.replace('(','').replace(')','').strip()
        #简介有些书没有，所有这里需要异常处理
        inq=''
        try:
            inq=item.select('.inq')[0].text
        except:
            pass
        #将信息加入字典
        dict.append({'bookname':bookName,'price':price,'time':time,'store':store,'autor':autor,'score':score,'pingjiaNum':pjNum,'inq':inq})
        dict1.append(inq)

#输出文件
allinfo=pandas.DataFrame(dict)
allinfo.to_excel('booktop250.xlsx')

#将字典格式转变成字符串并写出，为分词做准备

dict1str='\n'.join(dict1)
with open(r'jianjie.txt','w',encoding='utf-8') as f:
    f.write(dict1str)
    f.close()
#分词
#定义一个字典来装分词的词语
dict2=[]
#打开需要切词的文件
with open(r'jianjie.txt','r',encoding='utf-8') as f:
    # 停用词加载,注意txt文件的编码格式
    stopword = [line.strip() for line in open(r'stopword.txt', 'r', encoding='utf-8').readlines()]
    for line1 in f.readlines():
        words=jieba.cut(line1.strip())
        for word in words:
            if word is not stopword:
                dict2.append(word)
dict2str='\n'.join(dict2)
#将切词文件写出
open(r'out.txt','w').write(dict2str)

'''
#词云生成
#词云属性设置：字体，图片大小
dict3=[]
with open(r'author.txt','r',encoding='utf-8') as f:
    for line in f.readlines():
        dict3.append(line.strip())
dict3str='\n'.join(dict3)

word_pic=WordCloud(font_path=r'simkai.ttf',width=1100,height=500).generate(dict3str)
plt.imshow(word_pic)
#去掉坐标轴
plt.axis('off')
#保存图片到位置
plt.savefig(r'author.png')
'''



