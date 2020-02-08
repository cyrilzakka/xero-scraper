# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy.pipelines.files import FilesPipeline

class XeroPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        original_path = re.search('studyUID=(.+?)&', request.url).group(1).split('.')[-2:]
        if re.search('seriesUID=(.+?)&', request.url) is not None:
            original_path = re.search('seriesUID=(.+?)&', request.url).group(1)
        root = re.search('studyUID=(.+?)&', request.url).group(1)
        if "objectUID" in request.url:
            return '%s/%s.jpeg' % (root, original_path)
        else:
            return '%s/%s.pdf' % (root, ".".join(original_path))


