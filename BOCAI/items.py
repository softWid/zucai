# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BocaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BocaiMatchItem(scrapy.Item):
    matchId = scrapy.Field()
    rowNo = scrapy.Field()
    typeName = scrapy.Field()
    matchTime = scrapy.Field()
    homeTeam = scrapy.Field()
    visitTeam = scrapy.Field()
    matchResult = scrapy.Field()
    createDate = scrapy.Field()

class BocaiMatchRateItem(scrapy.Item):
    matchId = scrapy.Field()
    cmpNo = scrapy.Field()
    newTime = scrapy.Field()
    newWin = scrapy.Field()
    newdraw = scrapy.Field()
    newLost = scrapy.Field()
    oldTime = scrapy.Field()
    oldWin = scrapy.Field()
    olddraw = scrapy.Field()
    oldLost = scrapy.Field()


class BocaiMatchGoalItem(scrapy.Item):
    matchId = scrapy.Field()
    homeGoal = scrapy.Field()
    homeLost = scrapy.Field()
    visitGoal = scrapy.Field()
    visitLost = scrapy.Field()
