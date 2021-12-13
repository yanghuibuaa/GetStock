# -*- coding: utf-8 -*-
import scrapy
#import requests
from scrapy import Request
from scrapy.spiders import CrawlSpider
import time
import datetime
import re
import json
from ZhihuSpider.items import QuesInfoItem

class ZhSpider(CrawlSpider):
    name = 'ZhSpider'
    allowed_domains = ['zhihu.com']
    # start_urls是Spider在启动时进行爬取的入口URL列表。第一个被获取到的页面的URL将是其中一个，
    # 后续的URL从初始的URL的响应中获取
    #start_urls = ['https://www.zhihu.com/r/search?q=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0',
    #'https://www.zhihu.com/r/search?q=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&correction=1&type=content&offset=30',
    #]
    #base_url = 'https://www.zhihu.com/people/excited-vczh/activities'
    base_url = 'https://www.zhihu.com/people/yanghui-92'
    #start_urls = ['https://www.zhihu.com/people/excited-vczh/activities']
    #start_urls = ['https://www.zhihu.com/api/v4/members/excited-vczh/activities?limit=7&session_id=1183758912434778112&after_id=1575445096&desktop=True']
    start_urls = ['https://www.zhihu.com/api/v3/moments/yanghui-92/activities?limit=7&session_id=1358733206741721089&after_id=1638511426&desktop=true']
    #start_urls = ['https://www.zhihu.com/api/v4/members/yanghui-92/activities?limit=7&session_id=1183758912434778112&after_id=1575445096&desktop=True']
    # parse是Spider的一个方法。被调用时，每个初始的URL响应后返回的response对象，将会作为唯一的参数返回给该方法
    # 该方法负责解析返回的数据（respose data）、提取数据（item）以及生成需要进一步处理的URL的Response对象
    
    #数字（1970年开始的秒数）转换为日期格式
    def timeStamp(timeNum):
        timeStamp = float(timeNum)
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        print (otherStyleTime)

    def parse(self, response):
        
        # print('***********************\n',response.body,'***********************\n\n')
        print('*************开始下载json文件:*********************')
        # 1、实现网页的解析，生成item
        # 首先打开js路径，获取'htmls'KEY下面的内容，是一个整体的str文件，没有标KEY，所以用re去解析它
        try:
            # print(type(response.body))
            # print(type(response.text))
            jsDict = json.loads(response.body)
            # print(type(jsDict))
            print('*************开始解析页面*********************')
            activities = jsDict['data']
            print(activities)
            # 抽取所有的问题和对应的follwer_num, answer_num和answer_abstract
            for q in activities:
                item = QuesInfoItem()
                # 删去源代码中关键词“<em>机器学习</em>”的标签
                #q = q.replace('<em>','').replace('</em>','')
                # 问题信息在标签 class=\"js-title-link\">和</a>当中
                #question = re.findall('class=\"js-title-link\">(.*?)</a>',q)[0]
                #print(q)
                #当日日期转换为1970秒数
                timeDateStr=str(datetime.date.today())
                time1=datetime.datetime.strptime(timeDateStr,"%Y-%m-%d")
                todaysecondsFrom1970=int(time.mktime(time1.timetuple()))
                print(todaysecondsFrom1970)
                print(q['created_time'])
                #只爬取当天的 
                '''
                if q['created_time'] < todaysecondsFrom1970:
                    print("非当日活动，爬虫结束！")
                    break
                '''
                
                #把1970秒数转换为日期字符串
                item['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(q['created_time']))) 
                item['action_text'] = q['action_text']
                if item['action_text'] == '赞同了回答':
                    item['content'] = q['target']['content']
                    item['question'] = q['target']['question']['title']
                elif item['action_text'] == '发布了想法':
                    item['content'] = q['target']['content']
                elif item['action_text'] == '回答了问题':
                    item['content'] = q['target']['content']
                    item['question'] = q['target']['question']['title']
                elif item['action_text'] == '关注了问题':
                    item['question'] = q['target']['title']
                elif item['action_text'] == '赞同了文章':
                    item['content'] = q['target']['content']
                    item['question'] = q['target']['title']
                yield item
                time.sleep(1)

            # 2、构造下一页的链接并回调给parse方法
            #first_url = 'https://www.zhihu.com/r/search?q=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0'
            # 下一页链接信息在js文件的['paging']标签下的['next']KEY中
            if q['created_time'] > todaysecondsFrom1970:
                print("当日活动，继续爬取下一页！")
                nexturl = jsDict['paging']['next']
                print("next url is---")
                print(nexturl)
                yield Request(nexturl, callback=self.parse) 

        except json.decoder.JSONDecodeError as e: #这个报错开始是因为找错了url一直报错加的，现在应该没关系可以去掉了
            print('JSONDecodeError')

