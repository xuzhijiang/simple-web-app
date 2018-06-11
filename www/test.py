from .models import User, Blog, Comment
from .orm import create_pool


def test():
	yield from create_pool(user='www-data', password='www-data', db='awesome')
	u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
	yield from u.save()

for x in test():
	pass
# 可以在MySQL客户端命令行查询，看看数据是不是正常存储到MySQL里面了。