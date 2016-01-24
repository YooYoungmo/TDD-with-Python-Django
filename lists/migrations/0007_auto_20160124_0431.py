# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0006_auto_20160123_2317'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='item',
            order_with_respect_to='list',
        ),
    ]
