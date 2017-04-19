from django.db import models
from django.utils import timezone


class ReportFile(models.Model):
    name = models.CharField(length=20)
    upload_time = models.DateTimeField('date uploaded', editable=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.upload_time = timezone.now()
        return super(ReportFile, self).save(*args, **kwargs)


class Report(models.Model):
    INAPPROPRIATE_TYPE_CHOICES = (
        ('ma', 'abuse_ma'),
        ('sell', 'abuse_sell'),
        ('cheat', 'abuse_cheat')
    )

    subject = models.CharField(max_length=150)
    description = models.TextField()
    inappropriate_type = models.CharField(choices=INAPPROPRIATE_TYPE_CHOICES, default=FRESHMAN)
    report_file = models.ForeignKey(ReportFile)

class SpoofAgent(models.Model):
    name = models.CharField(max_length=200)
    report = models.ForeignKey(Report)

class Agent(models.Model):
    name = models.CharField(max_length=200)    

class ReportRecord(models.Model):
    agent = models.ForeignKey(Agent)
    spoofAgent = models.ForeignKey(SpoofAgent)
    report_time = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.report_time = timezone.now()
        return super(ReportRecord, self).save(*args, **kwargs)

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
