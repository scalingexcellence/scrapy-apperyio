# Copyright 2013-14 Dimitrios Kouzis-Loukas <info@scalingexcellence.co.uk>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Appery.io Database Pipeline for scrapy"""

from twisted.internet import defer
from scrapy.http import Request
from urllib import urlencode
from scrapy import signals
import json


class ApperyIoPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings
        self.session = None

        crawler.signals.connect(
            self.spider_opened,
            signal=signals.spider_opened
        )

    def spider_opened(self, spider):
        request = Request(
            "https://api.appery.io/rest/1/db/login?{0}".format(urlencode({
                "username": self.settings.get('APPERYIO_USERNAME'),
                "password": self.settings.get('APPERYIO_PASSWORD')
            })),
            headers={
                "X-Appery-Database-Id": self.settings.get('APPERYIO_DB_ID')
            }
        )
        self.session = self.crawler.engine.download(request, spider)
        self.session.addCallback(lambda r: json.loads(r.body)['sessionToken'])

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        session = yield self.session

        flat_item = dict([(k, v and v[0] or None) for k, v in item.items()])

        request = Request(
            "https://api.appery.io/rest/1/db/collections/{0}".format(
                self.settings.get('APPERYIO_COLLECTION_NAME')
            ),
            method='POST',
            headers={
                'Content-type': 'application/json',
                'X-Appery-Database-Id': self.settings.get('APPERYIO_DB_ID'),
                'X-Appery-Session-Token': session
            },
            body=json.dumps(flat_item, default=lambda x: None)
        )
        yield self.crawler.engine.download(request, spider)

        defer.returnValue(item)
