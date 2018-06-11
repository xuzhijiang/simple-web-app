__author__ = 'Zhijiang Xu'

import asyncio, os, inspect, logging, functools
from urllib import parse
from aiohttp import web
from .apis import APIError

def get(path):
	'''
	Define decorator @get('/path')
	'''
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			return func(*args, **kw)
		wrapper.__method__ = 'GET'
		wrapper.__route__ = path
		return wrapper
	return decorator

def post(path):
    '''
    Define decorator @post('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator

def get_required_kw_args(fn):
	args = []
	params = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
			args.append(name)
	return tuple(args)


def get_named_kw_args(fn):
	args = []
	params = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY:
			args.append(name)
	return tuple(args)

def has_named_kw_args(fn):
	params = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY:
			return True

def has_var_kw_arg(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True

def has_request_arg(fn):
    sig = inspect.signature(fn)
    # logging.info('sig=====>%s' % str(sig))
    # logging.info('sig=====>%s' % sig)
    params = sig.parameters
    # logging.info('sig.parameters====>%s' % sig.parameters)
    #logging.info('sig.parameters====>%s' % sig.parameters['request'])
    #logging.info('sig.parameters====>%s' % sig.parameters['request'].annotation)
    found = False
    for name, param in params.items():
        # logging.info('param-------------%s' % param)
        # logging.info('param.kind--------%s' % param.kind)
        if name == 'request':
            found = True
            continue
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError('request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found


class RequestHandler(object):

    def __init__(self, app, fn):
        # logging.info('fn======>%s' % fn)
        self._app = app
        self._func = fn
        #是否有request参数
        self._has_request_arg = has_request_arg(fn)
        #是否有可变关键字参数
        self._has_var_kw_arg = has_var_kw_arg(fn)
        #是否有命名关键字参数
        self._has_named_kw_args = has_named_kw_args(fn)
        #得到命名关键字参数
        self._named_kw_args = get_named_kw_args(fn)
        #得到required参数
        self._required_kw_args = get_required_kw_args(fn)

    async def __call__(self, request):
        logging.info('request is %s' % request)
        logging.info('%s(%s)' % (self._func.__name__, ', '.join(inspect.signature(self._func).parameters.keys())))
        kw = None
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            logging.info('......search arg==01.....')
            if request.method == 'POST':
                if not request.content_type:
                    #指的是请求的内容类型
                    return web.HTTPBadRequest('Missing Content-Type.')
                ct = request.content_type.lower()
                if ct.startswith('application/json'):
                    #The MIME media type for JSON text is application/json.
                    #JSON文本的MIME媒体类型是application / json。
                    params = await request.json()
                    logging.info('request.json() is %s' % request.json())
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest('JSON body must be object.')
                    kw = params
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    params = await request.post()
                    kw = dict(**params)
                    #**kw是关键字参数，kw接收的是一个dict。
                    # 又可以先组装dict，再通过**kw传入：func(**{'a': 1, 'b': 2})。
                else:
                    return web.HTTPBadRequest('Unsupported Content-Type: %s' % request.content_type)
            if request.method == 'GET':
                qs = request.query_string
                logging.info('query_string is %s' % qs)
                if qs:
                    kw = dict()
                    for k, v in parse.parse_qs(qs, True).items():
                        kw[k] = v[0]
        if kw is None:
            logging.info('kw is none.......')
            logging.info('request.match_info is %s' % request.match_info)
            kw = dict(**request.match_info)
            logging.info('kw is %s' % kw)
        else:
            logging.info('kw is not none.....')
            if not self._has_var_kw_arg and self._named_kw_args:
                # remove all unamed kw:
                copy = dict()
                for name in self._named_kw_args:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            # check named arg:
            for k, v in request.match_info.items():
                if k in kw:
                    logging.warning('Duplicate arg name in named arg and kw args: %s' % k)
                kw[k] = v
        if self._has_request_arg:
            kw['request'] = request
        # check required kw:
        if self._required_kw_args:
            for name in self._required_kw_args:
                if not name in kw:
                    return web.HTTPBadRequest('Missing argument: %s' % name)
        logging.info('call with args: %s' % str(kw))
        try:
            r = await self._func(**kw)
            return r
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)

def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))

def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    #logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))

def add_routes(app, module_name):
    logging.info('coreweb....add_routes')
    n = module_name.rfind('.')
    if n == (-1):
        #>>> __import__('handlers',globals(),locals())
        #<module 'handlers' from '/mnt/c/Users/xu/Desktop/ZX/code/awesome-python3-webapp/www/handlers.py'>
        mod = __import__(module_name, globals(), locals())
        #logging.info('mod=======>%s' % mod)
    else:
        name = module_name[n+1:]
        logging.info('name is %s' % name)
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    #logging.info('mod is %s' % mod)
    #logging.info('mod is %s' % dir(mod))
    for attr in dir(mod):
        #>>> dir(__import__('handlers', globals(),locals()))
        #['Blog', 'Comment', 'User', '__author__', '__builtins__', 
        #'__cached__', '__doc__', '__file__', '__loader__', '__name__', 
        #'__package__', '__spec__', 'asyncio', 'base64', 'get', 'hashlib', 
        #'index', 'json', 'logging', 'next_id', 'post', 're', 'time']
        #logging.info('attr is %s' % attr)
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        #logging.info('fn===>%s' % fn)
        if callable(fn):
            #logging.info('fn is callable: %s' % fn)
            method = getattr(fn, '__method__', None)
            #logging.info('method=======>%s' % method)
            path = getattr(fn, '__route__', None)
            #logging.info('path========>%s' % path)
            if method and path:
                add_route(app, fn)
