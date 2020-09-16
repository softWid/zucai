# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import datetime
import logging
from BOCAI import settings
from functools import reduce


class BocaiPipeline(object):
	def process_item(self, item, spider):
		return item


class BocaiMatchPipeline(object):
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

	def process_item(self, item, spider):
		try:
			self.cursor.execute(
				'insert into footMatch (matchId, rowNo, typeName, matchTime, homeTeam, visitTeam, matchResult, createdate)  values (%s, %s, %s, %s, %s, %s, %s, %s)',
				(pymysql.escape_string(item['matchId']),
				 pymysql.escape_string(item['rowNo']),
				 pymysql.escape_string(item['typeName']),
				 pymysql.escape_string(item['matchTime']),
				 pymysql.escape_string(item['homeTeam']),
				 pymysql.escape_string(item['visitTeam']),
				 pymysql.escape_string(item['matchResult']),
				 pymysql.escape_string(item['createDate'])
				 ))
			self.connect.commit()
		except Exception:
			logging.log('插入数据库错误')

	def close_spider(self, spider):
		self.connect.close()


class BocaiMatchRatePipeline(object):
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

	def process_item(self, item, spider):
		try:
			self.cursor.execute(
				'insert into matchRate (matchId, cmpNo, oldTime, oldWin, olddraw, oldLost, newTime, newWin, newdraw, newLost)  values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE matchId=(%s) and cmpNo=(%s)',
				(pymysql.escape_string(item['matchId']),
				 pymysql.escape_string(item['cmpNo']),
				 pymysql.escape_string(item['oldTime']),
				 pymysql.escape_string(item['oldWin']),
				 pymysql.escape_string(item['olddraw']),
				 pymysql.escape_string(item['oldLost']),
				 pymysql.escape_string(item['newTime']),
				 pymysql.escape_string(item['newWin']),
				 pymysql.escape_string(item['newdraw']),
				 pymysql.escape_string(item['newLost']),
				 pymysql.escape_string(item['matchId']),
				 pymysql.escape_string(item['cmpNo'])
				 ))
			self.connect.commit()
		except Exception:
			logging.log('插入数据库错误')

	def close_spider(self, spider):
		self.connect.close()

	def StrToFloat2(self, Str):
		def str2num(Str):
			DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
			return DIGITS[Str]

		i = Str[::-1].index('.')
		s = Str.split('.')
		s1 = reduce(lambda x, y: x * 10 + y, map(str2num, s[0]))
		s2 = reduce(lambda x, y: x * 10 + y, map(str2num, s[1])) / 10 ** i
		return s1 + s2


class BocaiMatchGoalPipeline(object):
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

	def process_item(self, item, spider):
		try:
			self.cursor.execute(
				'insert into matchGoal (matchId, homeGoal, homeLost, visitGoal, visitLost)  values (%s, %s, %s, %s, %s) ',
				(pymysql.escape_string(item['matchId']),
				 pymysql.escape_string(item['homeGoal']),
				 pymysql.escape_string(item['homeLost']),
				 pymysql.escape_string(item['visitGoal']),
				 pymysql.escape_string(item['visitLost'])
				 ))
			self.connect.commit()
		except Exception:
			logging.log('插入数据库错误')

	def close_spider(self, spider):
		self.connect.close()
