from models import User, Blog, Comment
from orm import create_pool


def test():
    yield from create_pool(user='www-data', password='www-data', db='awesome')
    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
    yield from u.save()


for x in test():
    pass
