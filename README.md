Description
===========
It's a pipeline which allows you to store scrapy items in appery.io database.

Install
=======
   pip install "ScrapyApperyIoDB"

Configure your settings.py:
----------------------------
    ITEM_PIPELINES = [
      'scrapyapperyio.ApperyIoPipeline',
    ]
    
    APPERYIO_DB_ID = '1234abcdef1234abcdef1234'
    APPERYIO_USERNAME = 'user'
    APPERYIO_PASSWORD = 'pass'
    APPERYIO_COLLECTION_NAME = 'collection'

Changelog
=========

0.1.0
initial release

Licence
=======
Copyright 2013 Dimitrios Kouzis-Loukas

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
