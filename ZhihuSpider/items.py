# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 关于每一个问题的信息
class QuesInfoItem(scrapy.Item):
	created_time = scrapy.Field() #活动类型
	action_text = scrapy.Field() #活动类型
	content = scrapy.Field() #内容
	question = scrapy.Field() #问题
	
class CommentInfoItem(scrapy.Item):
	name = scrapy.Field() #评论者姓名
	bio = scrapy.Field() #评论者简介
	url = scrapy.Field() #评论者主页url
	content = scrapy.Field() #评论内容
