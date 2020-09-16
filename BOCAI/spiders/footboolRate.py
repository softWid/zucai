# -*- coding: utf-8 -*-
import datetime
import scrapy
import pymysql
import logging
from BOCAI import settings
from BOCAI import items


class FootboolrateSpider(scrapy.Spider):
	name = 'footboolRate'
	allowed_domains = ['woxaingwan.com']
	start_urls = ['http://woxaingwan.com/']
	custom_settings = {'ITEM_PIPELINES': {'BOCAI.pipelines.BocaiMatchRatePipeline': 500}}
	def __init__(self):
			self.connect = pymysql.connect(
				host=settings.MYSQL_HOST,
				db=settings.MYSQL_DBNAME,
				user=settings.MYSQL_USER,
				passwd=settings.MYSQL_PASSWD,
				charset='utf8',
				use_unicode=True
			)
			self.cursor = self.connect.cursor()

	def start_requests(self):
		createDate = datetime.datetime.now().strftime('%Y-%m-%d')
		nexrPara = ['2', '5', '7']
		try:
			result = self.cursor.execute('select matchId from footmatch where createDate=(%s) ',
										pymysql.escape_string(createDate))
			if result:
				for re in range(result):
					print('###################################')
					matchId = str(self.cursor.fetchone()[0])
					url = 'http://www.woxiangwan.com/zcj/jincai/peilvhis?flag=qb&rowNo=' + matchId
					for para in nexrPara:
						newUrl = url+'&cmpNo='+para
						print(newUrl)
						yield scrapy.Request(newUrl, meta={'matchId':matchId,'cmpNo':para},callback=self.parse)
		except Exception as error:
			logging.log('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
		finally:
			self.cursor.close()



	#/div[@class ="subItem"]   extract
	def parse(self, response):
		text = response.xpath('//div[@class="tabList"]')
		ab = text.xpath('./div/div/span').extract()
		item = items.BocaiMatchRateItem()
		item['matchId'] = response.meta['matchId']
		item['cmpNo'] = response.meta['cmpNo']
		item['newTime'] = self.dropSpan(ab[0])
		item['newWin'] = self.dropSpan(ab[1])
		item['newdraw'] = self.dropSpan(ab[2])
		item['newLost'] = self.dropSpan(ab[3])
		item['oldTime'] = self.dropSpan(ab[-4])
		item['oldWin'] = self.dropSpan(ab[-3])
		item['olddraw'] = self.dropSpan(ab[-2])
		item['oldLost'] = self.dropSpan(ab[-1])
		yield item


	#去掉<span>标签
	def dropSpan(self,str):
		return str.lstrip('<span>').rstrip('</span>')

