# -*- coding: utf-8 -*-
import scrapy
import datetime
import pymysql
import logging
from BOCAI import settings
from BOCAI import items


class MatchgoalSpider(scrapy.Spider):
	name = 'matchgoal'
	allowed_domains = ['woxiangwan.com']
	custom_settings = {'ITEM_PIPELINES': {'BOCAI.pipelines.BocaiMatchGoalPipeline': 600}}
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
		try:
			result = self.cursor.execute('select matchId from footmatch where createDate=(%s) ',
										 pymysql.escape_string(createDate))
			if result:
				for re in range(result):
					print('###################################')
					matchId = str(self.cursor.fetchone()[0])
					url = 'http://www.woxiangwan.com/zcj/matchinfo/info?matchid=' + matchId
					yield scrapy.Request(url, meta={'matchId':matchId}, callback=self.parse)
		except Exception:
			logging.log('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
		finally:
			self.cursor.close()


	def parse(self, response):
		item = items.BocaiMatchGoalItem()
		home = response.xpath('//div[@class="gol-fba"]')[2]
		visit = response.xpath('//div[@class="gol-fba"]')[5]
		homeGoal = home.xpath('./div[@class="s-heng gol-fb"]/div[2]/text()').extract()[0]
		homeLost =  home.xpath('./div[@class="s-heng gol-fb"]/div[2]/text()').extract()[1]
		visitGoal = visit.xpath('./div[@class="s-heng gol-fb"]/div[2]/text()').extract()[0]
		visitLost = visit.xpath('./div[@class="s-heng gol-fb"]/div[2]/text()').extract()[1]
		item['matchId'] = response.meta['matchId']
		item['homeGoal'] =  homeGoal
		item['homeLost'] = homeLost
		item['visitGoal'] = visitGoal
		item['visitLost'] = visitLost
		yield item




