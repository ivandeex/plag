from django.db import models


class Proxy(models.Model):
    source = models.CharField('source', max_length=10)
    scraped_at = models.DateTimeField('scraped at')
    updated_at = models.DateTimeField('updated at')
    country = models.CharField('country', max_length=24)
    ip_addr = models.CharField('ip address', max_length=16)
    port = models.IntegerField('port')
    proto = models.CharField('protocol', max_length=5)
    anonimity = models.CharField('anonimity', max_length=8)
    speed_qual = models.IntegerField('speed quality')
    connect_qual = models.IntegerField('connect quality')

    def __str__(self):
        return u'{}:{} {} ({})'.format(self.ip_addr, self.port, self.proto, self.source)

    class Meta:
        verbose_name = 'proxy'
        verbose_name_plural = 'proxies'
        unique_together = (('ip_addr', 'port', 'source'),)

    @classmethod
    def from_json(cls, data):
        kwargs = dict(source=data['source'], ip_addr=data['ip_addr'], port=data['port'])
        try:
            obj = cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            obj = cls(**kwargs)

        for field, value in data.items():
            setattr(obj, field, value)

        obj.save()
        return obj
