from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


@python_2_unicode_compatible
class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ('list', 'text')


