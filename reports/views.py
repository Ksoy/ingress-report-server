import json
import os
import ntpath

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from .models import Agent, Cheater, Report, ReportCheater, ReportFile, ReportRecord

INAPPROPRIATE_MAP = {
    'abuse_ma': 'Multiple accounts/account sharing',
    'abuse_sell': 'Account buying/selling',
    'abuse_cheat': 'GPS spoofing'
}

STATUS = [
  'new', 'close', 'delete', 
]

def home(request):
    return render(request, 'home.html') 

def list(request):
    """List all reports page."""

    cheater_list = Cheater.objects.all()
    for cheater in cheater_list:
        report_cheater_list = ReportCheater.objects.filter(cheater=cheater).order_by('report')
        count = 0
        for report_cheater in report_cheater_list:
            record = ReportRecord.objects.filter(report_cheater=report_cheater)
            count += len(record)
        report_record = {'reports': len(report_cheater_list), 'count': count}
        cheater.report_record = report_record
    context = {
        'cheater_list': cheater_list,
    }
    return render(request, 'list.html', context)

@login_required(login_url='/reports/v1/login')
def manage_report(request):
    """Report management page."""
    report_list = Report.objects.all()
    for report in report_list:
        report.inappropriate_type = INAPPROPRIATE_MAP[report.inappropriate_type]
        report_cheaters = ReportCheater.objects.filter(report=report)
        report.cheaters = [rc.cheater for rc in report_cheaters]
    context = {
        'report_list': report_list,
    }
    return render(request, 'admin.html', context)

@login_required(login_url='/reports/v1/login')
def manage_user(request):
    """User management page."""
    return render(request, 'admin.html')

@login_required(login_url='/reports/v1/login')
def edit_report(request, r_id=None):
    context = {
        'INAPPROPRIATE_MAP': INAPPROPRIATE_MAP,
        'STATUS': STATUS,
        'report': { 'status': 'new'},
    }
    if r_id:
        report = Report.objects.get(id=r_id)
        reportcheater_list = ReportCheater.objects.filter(report=report)
        report.cheaters = ', '.join([rc.cheater.name for rc in reportcheater_list])
        context['report'] = report
    return render(request, 'manage.html', context)
