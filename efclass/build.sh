#!/bin/bash
virtualenv -p /usr/bin/python .
bin/pip install -r requirements.txt -i http://pypi.douban.com/simple
