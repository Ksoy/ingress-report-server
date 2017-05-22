from django.db import models
from django.utils import timezone
import uuid
import os

def user_directory_path(instance, filename):
    instance.ori_name = filename
    _, ext = os.path.splitext(filename)
    return '{}{}'.format(str(uuid.uuid4()), ext)

class ReportFile(models.Model):
    upload_file = models.FileField(upload_to=user_directory_path)
    ori_name = models.CharField(max_length=50)
    upload_time = models.DateTimeField('date uploaded', editable=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.upload_time = timezone.now()
        return super(ReportFile, self).save(*args, **kwargs)


class Report(models.Model):
    INAPPROPRIATE_TYPE_CHOICES = (
        ('abuse_ma', 'abuse_ma'),
        ('abuse_sell', 'abuse_sell'),
        ('abuse_cheat', 'abuse_cheat')
    )

    STATUS_CHOICES = (
        ('new', 'new'),
        ('close', 'close'),
    )

    subject = models.CharField(max_length=150)
    description = models.TextField()
    inappropriate_type = models.CharField(max_length=20, choices=INAPPROPRIATE_TYPE_CHOICES)
    report_file = models.ForeignKey(ReportFile)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    cheaters = []

class Cheater(models.Model):
    STATUS_CHOICES = (
        ('new', 'new'),
        ('burned', 'burned'),
    )

    name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    report_record = {}

class ReportCheater(models.Model):
    report = models.ForeignKey(Report)
    cheater = models.ForeignKey(Cheater)

class Agent(models.Model):
    name = models.CharField(max_length=200)    

class ReportRecord(models.Model):
    agent = models.ForeignKey(Agent)
    report_cheater = models.ForeignKey(ReportCheater)
    report_time = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.report_time = timezone.now()
        return super(ReportRecord, self).save(*args, **kwargs)

