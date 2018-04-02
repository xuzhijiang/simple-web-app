#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Default configurations.
'''
import logging

__author__ = 'Zhijiang Xu'

configs = {
	'debug': True,
	'db' : {
		'host': '127.0.0.1',
		'port': 3306,
		'user': 'www',
		'password': 'www',
		'db': 'awesome'
	},
	'session': {
		'secret': 'Awesome'
	}
}
logging.info('__file__ is %s' % __file__)