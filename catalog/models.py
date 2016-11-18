from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class catalogModel(models.Model):
    class Meta:
        managed=False
        permissions = (
            ('catalog_admin', 'Catalog Admin'),
            ('catalog_create','Create Catalog Collections'),
        )
