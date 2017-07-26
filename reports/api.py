import json
import os
import ntpath

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from .models import Agent, Cheater, Report, ReportCheater, ReportFile, ReportRecord
from .config import INAPPROPRIATE_MAP, EXTENSION_VERSION

@login_required(login_url='/reports/v1/login')
def user_list(request):
    data = {
      'users': []
    }
    for user in User.objects.all():
        user_data = {
            'id': user.id,
            'username': user.username,
            'is_superuser': user.is_superuser,
        }
        data['users'].append(user_data)

    return HttpResponse(json.dumps(data))

def cheater_list(request):
    data = {
      'cheaters': []
    }
    for cheater in Cheater.objects.filter()[::-1]:
        report_cheaters = ReportCheater.objects.filter(cheater=cheater).order_by('report')
        times = 0
        for report_cheater in report_cheaters:
            record = ReportRecord.objects.filter(report_cheater=report_cheater)
            times += len(record)
        cheater_data = {
            'id': cheater.id,
            'name': cheater.name,
            'status': cheater.status,
            'report_times': times,
            'report_count': len(report_cheaters)
        }
        data['cheaters'].append(cheater_data)
        
    return HttpResponse(json.dumps(data))

@login_required(login_url='/reports/v1/login')
def report_list(request):
    """Reutn all report information."""
    data = {
        'reports': []
    }
    for report in Report.objects.filter()[::-1]:
        filename = None
        if report.report_file:
            filename = report.report_file.upload_file.name
        report_data = {
            'report_id': report.id,
            'subject': report.subject,
            'description': report.description,
            'cheaters': [],
            'inappropriate_type': INAPPROPRIATE_MAP[report.inappropriate_type],
            'filename': filename,
            'status': report.status,
            'creator': report.creator.username,
            'create_time': report.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for report_cheater in ReportCheater.objects.filter(report=report):
            status = report_cheater.cheater.status
            cheater = {
                'cheater_id': report_cheater.cheater.id,
                'name': report_cheater.cheater.name,
                'status': report_cheater.cheater.status,
            }
            report_data['cheaters'].append(cheater)

        data['reports'].append(report_data)
	
    return HttpResponse(json.dumps(data))

def agent_report_list(request, user):
    """Reutn all report information."""
    data = {
        'reports': []
    }
    for report in Report.objects.filter(status='new'):
        filename = None
        if report.report_file:
            filename = report.report_file.upload_file.name
        report_data = {
            'report_id': report.id,
            'subject': report.subject,
            'description': report.description,
            'cheaters': [],
            'inappropriate_type': report.inappropriate_type,
            'filename': filename,
            'status': report.status,
            'creator': report.creator.username,
        }
        flag = False
        for report_cheater in ReportCheater.objects.filter(report=report):
            if 'alive' == report_cheater.cheater.status:
                try:
                    agent = Agent.objects.get(name=user)
                    records = ReportRecord.objects.filter(agent=agent, report_cheater=report_cheater)
                    if len(records) > 0:
                        continue
                except:
                    pass
                flag = True
                cheater = {
                    'cheater_id': report_cheater.cheater.id,
                    'name': report_cheater.cheater.name,
                    'status': report_cheater.cheater.status,
                }
                report_data['cheaters'].append(cheater)
        if flag:
            data['reports'].append(report_data)
	
    return HttpResponse(json.dumps(data))

def record(request, agent_name, report_id, cheater_name):
    """Record agent report spoofagent history."""
    try:
        agent, created = Agent.objects.get_or_create(name=agent_name)
        agent.save()
        cheater = Cheater.objects.filter(name=cheater_name)
        report = Report.objects.filter(id=report_id)
        report_cheater = ReportCheater.objects.filter(report=report[0], cheater=cheater[0])
        report_record = ReportRecord(agent=agent, report_cheater=report_cheater[0])
        report_record.save()
    except:
        return HttpResponse('false')

    return HttpResponse('ok')

@login_required(login_url='/reports/v1/login')
def save_report(request):
    if request.method == 'POST':
        if request.POST.get('report_id'):
            report = Report.objects.get(id=request.POST.get('report_id'))
        else:
            report = Report(creator=request.user)

        report.subject = request.POST.get('subject')
        report.description = request.POST.get('description')
        report.inappropriate_type = request.POST.get('inappropriate_type')
        report.status = request.POST.get('status')

        if len(request.FILES):
            report_file = ReportFile(upload_file=request.FILES['upload_file'])
            report_file.save()
            report.report_file = report_file
        report.save()

        cheater_list = request.POST.get('cheaters').split(',')
        for cheater_name in cheater_list:
            if not cheater_name.strip():
                continue
            cheater, is_create = Cheater.objects.get_or_create(name=cheater_name.strip())
            cheater.save()
            reportcheater, is_create = ReportCheater.objects.get_or_create(cheater=cheater, report=report)
            reportcheater.save()

        return redirect('reports:reports_page')
    return HttpResponse(status=404)

@login_required(login_url='/reports/v1/login')
def update_cheater(request):
    cheater_id = request.POST.get('cheater_id')
    status = request.POST.get('status')

    cheater = Cheater.objects.get(id=cheater_id)
    cheater.status = status
    cheater.save()
   
    reportcheaters = ReportCheater.objects.filter(cheater=cheater)
    for rc in reportcheaters:
        rcs = ReportCheater.objects.filter(report=rc.report)
        flag = True
        for rc_ in rcs:
            if rc_.cheater.status == 'alive':
                flag = False
                break
        if flag:
            rc.report.status = 'close'
            rc.report.save()

    return HttpResponse('ok')

def extension_version(request):
    return HttpResponse(EXTENSION_VERSION)
