#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Zhijiang Xu'

#先执行config_default脚本
from .config_default import configs
import logging

class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            logging.info('key is %s' % key)
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
# 如果字符串里面有很多字符都需要转义，就需要加很多\，
# 为了简化，Python还允许用r''表示''内部的字符串默认不转义，可以自己试试：
# >>> print('\\\t\\')
# \       \
# >>> print(r'\\\t\\')
# \\\t\\

    def __setattr__(self, key, value):
        self[key] = value

def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D
logging.info('__file__ is %s' % __file__)

#override default Configuration
try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

#把configs中的dict转换成我们自己定义的Dict
configs = toDict(configs)