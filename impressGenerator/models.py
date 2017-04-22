import os
from html import escape

from django.db import models


class Page(models.Model):
    page_src = models.TextField()
    page_order = models.SmallIntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    rx = models.SmallIntegerField()
    ry = models.SmallIntegerField()
    rz = models.SmallIntegerField()
    scale = models.SmallIntegerField()
    presentation = models.ForeignKey('Presentation')

    @property
    def rendered(self):
        # todo:add some rendering code in the future
        ret = escape(self.page_src)
        ret = ret.replace(' ', '&nbsp;')
        return ret

    def __str__(self):
        ret = '(' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ')'
        ret += self.page_src[:10] + ('...' if len(self.page_src) > 10 else '')
        return ret

    @property
    def summary(self):
        return str(self)


def random_token():
    return str(os.urandom(24)).replace('\\x', '')[2:-1]


class Presentation(models.Model):
    name = models.TextField()
    token = models.CharField(max_length=64, default=random_token)

    def __str__(self):
        return self.name
