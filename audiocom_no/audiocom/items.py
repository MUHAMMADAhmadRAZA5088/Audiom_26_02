# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
"""Provides some arithmetic functions"""
import scrapy
class AudiocomItem(scrapy.Item):
    '''Takes in a number n, returns the square of n'''
    # define the fields for your item here like:
    name = scrapy.Field()
    features=scrapy.Field()
    price = scrapy.Field()
    img = scrapy.Field()
