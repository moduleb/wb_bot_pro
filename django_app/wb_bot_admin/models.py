# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class All(models.Model):
    user_id = models.BigIntegerField(blank=True, null=True)
    item_id = models.BigIntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    title = models.CharField(blank=True, null=True)
    url = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'all_'
