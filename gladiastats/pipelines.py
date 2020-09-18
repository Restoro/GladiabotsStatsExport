# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import io
import os
import six

from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from scrapy.utils.project import get_project_settings

from zope.interface import implementer
from scrapy.extensions.feedexport import IFeedStorage
from w3lib.url import file_uri_to_path

class GladiastatsPipeline(object):
    def process_item(self, item, spider):
        return item