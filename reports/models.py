from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
import uuid
import os

def user_file_name(instance, filename):
    instance.ori_name = filename
    _, ext = os.path.splitext(filename)
    return '{}{}'.format(str(uuid.uuid4()), ext)

class ReportFile(models.Model):
    upload_file = models.FileField(upload_to=user_file_name)
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
    report_file = models.ForeignKey(ReportFile, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    cheaters = []

    create_time = models.DateTimeField(editable=False)
    creator = models.ForeignKey(User, editable=False)
    expire_date = models.DateField(null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.create_time = timezone.now()
            self.expire_date = timezone.now() + timedelta(days=3)
        return super(Report, self).save(*args, **kwargs)

class Cheater(models.Model):
    STATUS_CHOICES = (
        ('new', 'new'),
        ('alive', 'alive'),
        ('burned', 'burned'),
    )

    name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='alive')

    create_time = models.DateTimeField(editable=False)
    burned_time = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.create_time = timezone.now()
        if 'burned' == self.status:
            self.burned_time = timezone.now()
        return super(Cheater, self).save(*args, **kwargs)

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

