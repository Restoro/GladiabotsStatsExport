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

    def open_spider(self, spider):
        self.file = open('stats.csv', 'w')

        self.exporter = MyCsvItemExporter(self.file)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.file.close()

        self.exporter.finish_exporting()

@implementer(IFeedStorage)
class FixedFileFeedStorage(object):

    def __init__(self, uri):
        self.path = file_uri_to_path(uri)

    def open(self, spider):
        dirname = os.path.dirname(self.path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        return open(self.path, 'ab')

    def store(self, file):
        file.close()

class MyCsvItemExporter(CsvItemExporter):

    def __init__(self, file, include_headers_line=True, join_multivalued=',', **kwargs):

        # Custom delimiter
        settings = get_project_settings()
        delimiter = settings.get('CSV_DELIMITER', ';')
        kwargs['delimiter'] = delimiter

        super(MyCsvItemExporter, self).__init__(file, include_headers_line, join_multivalued, **kwargs)

        self._configure(kwargs, dont_fail=True)
        self.stream.close()
        storage = FixedFileFeedStorage(file.name)
        file = storage.open(file.name)
        self.stream = io.TextIOWrapper(
            file,
            line_buffering=False,
            write_through=True,
            encoding=self.encoding,
            newline="",
        ) if six.PY3 else file
        self.csv_writer = csv.writer(self.stream, **kwargs)