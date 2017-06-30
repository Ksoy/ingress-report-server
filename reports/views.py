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
from .config import INAPPROPRIATE_MAP, REPORT_STATUS_LIST

def home(request):
    return render(request, 'home.html') 

def cheaters(request):
    return render(request, 'cheater_list.html')

@login_required(login_url='/reports/v1/login')
def reports(request):
    return render(request, 'report_list.html')

@login_required(login_url='/reports/v1/login')
def users(request):
    return render(request, 'user_list.html')

@login_required(login_url='/reports/v1/login')
def report_manage(request, r_id=None):
    context = {
        'INAPPROPRIATE_MAP': INAPPROPRIATE_MAP,
        'STATUS': REPORT_STATUS_LIST,
        'report': { 'status': 'new'},
    }
    if r_id:
        report = Report.objects.get(id=r_id)
        reportcheater_list = ReportCheater.objects.filter(report=report)
        report.cheaters = ', '.join([rc.cheater.name for rc in reportcheater_list])
        context['report'] = report
    return render(request, 'report_manage.html', context)
