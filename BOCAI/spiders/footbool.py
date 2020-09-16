# -*- coding: utf-8 -*-
import scrapy
import json
import sys
import  datetime
sys.path.append('../')
from BOCAI import items

class FootboolSpider(scrapy.Spider):
	name = 'footbool'
	allowed_domains = ['woxiangwan.com']
	start_urls = ['http://www.woxiangwan.com/zcj/jincai/getAllMatchList']
	custom_settings = {'ITEM_PIPELINES': {'BOCAI.pipelines.BocaiMatchPipeline': 300}}
	def parse(self, response):
		date = json.loads(response.text)
		# with open('./a.txt','w',encoding='UTF-8') as  f:
		# 	f.write(response.text)
		rows = date.get('rows')
		item =items.BocaiMatchItem()
		dayOfWeek =self.getDayOfWeek()
		createDate = datetime.datetime.now().strftime('%Y-%m-%d')
		print('################################################')
		for row in rows:
			if dayOfWeek in row.get('rowNo') and row.get('matchLong') == '未':
				item['matchId'] = row.get('matchId')
				item['rowNo'] = row.get('rowNo')
				item['typeName'] = row.get('typeName')
				item['matchTime'] = row.get('matchTime')
				item['homeTeam'] = row.get('homeTeam')
				item['visitTeam'] = row.get('visitTeam')
				item['matchResult'] = row.get('matchResult')
				item['createDate'] = createDate
				yield item

	def getDayOfWeek(self):
		dayOfWeek = datetime.datetime.now().strftime("%w")
		weekday = {'0': '周日', '1': '周一', '2': '周二', '3': '周三', '4': '周四', '5': '周五', '6': '周六'}
		return weekday.get(dayOfWeek)