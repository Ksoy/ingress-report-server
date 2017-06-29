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

# Create your views here.
def home_page(request):
    return render(request, 'home.html') 

def list_page(request):
    """List all reports page."""

    cheater_list = Cheater.objects.all()
    for cheater in cheater_list:
        report_cheater_list = ReportCheater.objects.filter(cheater=cheater).order_by('report')
        report_record = []
        for report_cheater in report_cheater_list:
            record = ReportRecord.objects.filter(report_cheater=report_cheater)
            report_record.append({'id': report_cheater.report.id, 'num': len(record)})
        cheater.report_record = report_record
    context = {
        'cheater_list': cheater_list,
    }
    return render(request, 'list.html', context)

def info_page(request, r_id):
    """Report infomation page."""

    report = Report.objects.get(id=r_id)
    report.inappropriate_type = INAPPROPRIATE_MAP[report.inappropriate_type]
    report_cheater_list = ReportCheater.objects.filter(report=report)
    report.cheaters = ', '.join([rc.cheater.name for rc in report_cheater_list])
    context = {
        'report': report
    }
    return render(request, 'info.html', context)

@login_required(login_url='/reports/v1/login')
def admin_page(request):
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
def manage_page(request, r_id=None):
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

###############################################################################
# api 

def api_list(request, user):
    """Reutn all report information."""
    data = {
        'reports': []
    }
    for report in Report.objects.filter():
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
        }
        for report_cheater in ReportCheater.objects.filter(report=report):
            status = report_cheater.cheater.status
            if status != 'burned':
                try:
                    agent = Agent.objects.get(name=user)
                    records = ReportRecord.objects.filter(agent=agent, report_cheater=report_cheater)
                    if len(records) > 0:
                        status = 'Done'
                except:
                    pass
            cheater = {
                'name': report_cheater.cheater.name,
                'status': status,
            }
            report_data['cheaters'].append(cheater)

        data['reports'].append(report_data)
	
    return HttpResponse(json.dumps(data))

def api_record(request, agent_name, report_id, cheater_name):
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
def api_save_report(request):
    if request.method == 'POST':
        if request.POST.get('report_id'):
            report = Report.objects.get(id=request.POST.get('report_id'))
        else:
            report = Report()

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
            cheater, is_create = Cheater.objects.get_or_create(name=cheater_name.strip())
            cheater.save()
            reportcheater, is_create = ReportCheater.objects.get_or_create(cheater=cheater, report=report)
            reportcheater.save()

        return redirect('reports:admin_page')
    return HttpResponse(status=404)

@login_required(login_url='/reports/v1/login')
def api_update_agent(request):
    c_id = request.POST.get('c_id')
    r_id = request.POST.get('r_id')
    status = request.POST.get('status')

    cheater = Cheater.objects.get(id=c_id)
    cheater.status = status
    cheater.save()
   
    reportcheaters = ReportCheater.objects.get(cheater=cheater)
    for rc in reportcheaters:
        rcs = ReportCheater.objects.get(report=rc.report)
        flag = True
        for rc_ in rcs:
            if tc_.cheater.status == 'new':
                flag = False
                break
        if flag:
            rc.report.status = 'close'
            rc.report.save()

    return HttpResponse('ok')
