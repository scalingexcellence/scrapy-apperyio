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

import json

from twisted.internet import defer
from scrapy.http import Request
from urllib import urlencode


class ApperyIoPipeline(object):
    DOWNLOAD_PRIORITY = 1000
    INSERT_ERROR_DISABLE_THRESHOLD = 5

    _session = None
    _attempt_login = None
    _active = False
    _total_errors = 0

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        o.crawler = crawler
        o.get_setting = crawler.settings.get
        return o

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        if not self._attempt_login:
            request = Request(
                "https://api.appery.io/rest/1/db/login?{0}".format(urlencode({
                    "username": self.get_setting('APPERYIO_USERNAME'),
                    "password": self.get_setting('APPERYIO_PASSWORD')
                })),
                headers={
                    "X-Appery-Database-Id": self.get_setting('APPERYIO_DB_ID')
                },
                priority=self.DOWNLOAD_PRIORITY
            )
            self._attempt_login = self.crawler.engine.download(request, spider)

            def extract_session(response):
                if response.status != 200:
                    raise RuntimeError("Unable to login: %s" % response.body)
                self._session = json.loads(response.body)['sessionToken']
                self._active = True

            self._attempt_login.addCallback(extract_session)

        yield self._attempt_login

        if self._active:

            flatitem = dict([(k, v and v[0] or None) for k, v in item.items()])

            request = Request(
                "https://api.appery.io/rest/1/db/collections/{0}".format(
                    self.get_setting('APPERYIO_COLLECTION_NAME')
                ),
                method='POST',
                headers={
                    'Content-type': 'application/json',
                    'X-Appery-Database-Id': self.get_setting('APPERYIO_DB_ID'),
                    'X-Appery-Session-Token': self._session
                },
                body=json.dumps(flatitem, default=lambda x: None),
                priority=self.DOWNLOAD_PRIORITY
            )

            response = yield self.crawler.engine.download(request, spider)
            logger = spider.logger
            if self._active and response.status != 200:
                logger.error('Failed to insert item to appery.io: %s' %
                             response.body)
                self._total_errors += 1
                if self._total_errors >= self.INSERT_ERROR_DISABLE_THRESHOLD:
                    logger.error('Too many errors: Disabling appery.io')
                    self._active = False

        defer.returnValue(item)
