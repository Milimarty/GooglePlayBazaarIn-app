from enum import IntEnum

from django.db import models


class Enum(IntEnum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Payment(models.Model):
    class Type(Enum):
        GooglePlay = 0
        Bazaar = 1

    type = models.PositiveSmallIntegerField(choices=Type.choices(), default=0)
    refresh_token = models.CharField(null=True, blank=True, max_length=255)
    scope = models.CharField(null=True, blank=True, max_length=255)
    token_type = models.CharField(null=True, blank=True, max_length=255)
    access_token = models.CharField(null=True, blank=True, max_length=255)
    init_token = models.CharField(null=True, blank=True, max_length=255)
    client_id = models.CharField(null=True, blank=True, max_length=255)
    client_secret = models.CharField(null=True, blank=True, max_length=255)
    redirect_url = models.CharField(null=True, blank=True, max_length=255)
    expires_in = models.BigIntegerField(null=True, blank=True, default=0)
