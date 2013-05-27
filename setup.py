from distutils.core import setup
setup(name='ScrapyApperyIoDB',
      version='0.1.0',
      license='Apache License, Version 2.0',
      description='Scrapy pipeline which allows you to store scrapy items in appery.io database.',
      author='Dimitrios Kouzis-Loukas',
      author_email='info@scalingexcellence.co.uk',
      url='http://github.com/scalingexcellence/scrapy-apperyio',
      keywords="scrapy apperyio",
      py_modules=['scrapyapperyio'],
      platforms = ['Any'],
      install_requires = ['scrapy', 'requests'],
      classifiers = [ 'Development Status :: 4 - Beta',
                      'Environment :: No Input/Output (Daemon)',
                      'License :: OSI Approved :: Apache Software License',
                      'Operating System :: OS Independent',
                      'Programming Language :: Python']
)
