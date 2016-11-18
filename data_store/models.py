from django.db import models

# Create your models here.

class dataStore(models.Model):
    class Meta:
        managed=False
        permissions = (
            ('datastore_admin', 'Data Store Admin'),
            ('datastore_create','Create DataStore Databases and Collections'),
        )
    pass
