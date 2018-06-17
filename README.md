#如何以最快的速度掌握编程，那就是不要复制，而是要自己敲


<!-- # 要执行INSERT、UPDATE、DELETE语句，可以定义一个通用的execute()函数，
# 因为这3种SQL的执行都需要相同的参数，以及返回一个整数表示影响的行数：
# execute()函数和select()函数所不同的是，cursor对象不返回结果集，
# 而是通过rowcount返回结果数。

# async def select(sql, args, size=None):
#     log(sql, args)
#     global __pool
#     async with __pool.get() as conn:
#         async with conn.cursor(aiomysql.DictCursor) as cur:
#             await cur.execute(sql.replace('?', '%s'), args or ())
#             if size:
#                 rs = await cur.fetchmany(size)
#             else:
#                 rs = await cur.fetchall()
#         logging.info('rows returned: %s' % len(rs))
#         return rs

# async def execute(sql, args, autocommit=True):
#     log(sql)
#     async with __pool.get() as conn:
#         if not autocommit:
#             await conn.begin()
#         try:
#             async with conn.cursor(aiomysql.DictCursor) as cur:
#                 await cur.execute(sql.replace('?', '%s'), args)
#                 affected = cur.rowcount
#             if not autocommit:
#                 await conn.commit()
#         except BaseException as e:
#             if not autocommit:
#                 await conn.rollback()
#             raise
#         return affected

# def person(name, age, *, city, job):
#     pass
# >>> person('jack',23)
# Traceback (most recent call last):
#   File "<pyshell#147>", line 1, in <module>
#     person('jack',23)
# TypeError: person() missing 2 required keyword-only arguments: 'city' and 'job'


# The Signature object represents the call signature of
#  a callable object and its return annotation. 
#  To retrieve a Signature object, use the signature() function.
# inspect.signature(callable, *, follow_wrapped=True) 
# Return a Signature object for the given callable:
# >>> from inspect import signature
# >>> def foo(a, *, b:int, **kwargs):
# ...     pass
# >>> sig = signature(foo)
# >>> str(sig)
# '(a, *, b:int, **kwargs)'
# >>> str(sig.parameters['b'])
# 'b:int'
# >>> sig.parameters['b'].annotation
# <class 'int'>

# getattr(object, name[, default]) 
# Return the value of the named attribute of object. 
# name must be a string. If the string is the name of 
# one of the object’s attributes, the result is the value of 
# that attribute. For example, getattr(x, 'foobar') is equivalent 
# to x.foobar. If the named attribute does not exist, default is 
# returned if provided, otherwise AttributeError is raised.
# 
#  callable(object) 
# Return True if the object argument appears callable, 
# False if not. If this returns true, it is still possible
#  that a call fails, but if it is false, calling object will
#   never succeed. Note that classes are callable (calling a 
#     class returns a new instance); instances are callable if 
#   their class has a __call__() method.
#   
#   @post('/api/blogs')
# def api_create_blog(request, *, name, summary, content):
#     check_admin(request)
#     if not name or not name.strip():
#         raise APIValueError('name', 'name cannot be empty.')
#     if not summary or not summary.strip():
#         raise APIValueError('summary', 'summary cannot be empty.')
#     if not content or not content.strip():
#         raise APIValueError('content', 'content cannot be empty.')
#     blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
#     yield from blog.save()
#     return blog
# name is request,
# POSITIONAL_OR_KEYWORD
# name is name,
# KEYWORD_ONLY
# name is summary,
# KEYWORD_ONLY
# name is content,
# KEYWORD_ONLY
 -->

<!-- # 为了简化，Python还允许用r''表示''内部的字符串默认不转义，可以自己试试： -->
