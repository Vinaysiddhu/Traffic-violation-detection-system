from django.db import models

# Create your models here.
class Speed_Detection(models.Model):
    SD_ID = models.AutoField(primary_key=True)
    VIDEO = models.FileField(upload_to='images/')

    class Meta:
        db_table = 'speed_detection'

class Helmet_Detection(models.Model):
    HD_ID = models.AutoField(primary_key=True)
    VIDEO = models.FileField(upload_to='images/')

    class Meta:
        db_table = 'helmet_detection'

class Tripleride_Detection(models.Model):
    TRD_ID = models.AutoField(primary_key=True)
    VIDEO = models.FileField(upload_to='images/')

    class Meta:
        db_table = 'tripleride_detection'

class SignalJump_Detection(models.Model):
    SJ_ID = models.AutoField(primary_key=True)
    VIDEO = models.FileField(upload_to='images/')

    class Meta:
        db_table = 'signaljump_detection'