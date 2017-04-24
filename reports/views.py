import json
import os
import ntpath

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from .models import SpoofAgent, Report, ReportRecord, Agent, ReportFile

INAPPROPRIATE_MAP = [
    {'name': 'abuse_ma', 'str': 'Multiple accounts/account sharing' },
    {'name': 'abuse_sell', 'str': 'Account buying/selling' },
    {'name': 'abuse_cheat', 'str': 'GPS spoofing' },
]

STATUS = [
  'new', 'close', 'delete', 
]

# Create your views here.
def home_page(request):
    return render(request, 'home.html') # HttpResponse("Hello, world. You're at the polls index.")

@login_required(login_url='/reports/v1/login')
def admin_page(request):
    """Report management page."""
    report_list = Report.objects.all()
    for report in report_list:
        agents = SpoofAgent.objects.filter(report=report)
        report.agents = [a for a in agents]
    context = {
        'report_list': report_list,
    }
    return render(request, 'admin.html', context)

def list_page(request):
    """List all reports page."""

    bad_agent_list = SpoofAgent.objects.all()
    #data = serializers.serialize("json", SpoofAgent.objects.filter(report_id=1))
    for bad_agent in bad_agent_list:
        record = ReportRecord.objects.filter(spoof_agent=bad_agent)
        bad_agent.numbers = len(record)
    context = {
        'bad_agent_list': bad_agent_list,
    }
    
    return render(request, 'list.html', context)

@login_required(login_url='/reports/v1/login')
def manage_page(request, r_id=None):
    context = {
        'INAPPROPRIATE_MAP': INAPPROPRIATE_MAP,
        'STATUS': STATUS,
        'report': { 'status': 'new'},
    }
    if r_id:
        report = Report.objects.get(id=r_id)
        bad_agent_list = SpoofAgent.objects.filter(report=report)
        report.agents = ', '.join([agent.name for agent in bad_agent_list])
        context['report'] = report
    return render(request, 'manage.html', context)

def api_list(request, user):
    """Reutn all report information."""
    data = {
        'reports': []
    }
    for report in Report.objects.all():
        filepath = None
        if report.report_file:
            filepath = '/reports/v1/{}'.format(report.report_file.upload_file.name)
        r = {
            'subject': report.subject,
            'description': report.description,
            'bad_agents': [],
            'inappropriate_type': report.inappropriate_type,
            'file_link': filepath,
        }
        for bad_agent in SpoofAgent.objects.filter(report=report):
            status = bad_agent.status
            if status != 'burn':
                try:
                    agent = Agent.objects.get(name=user)
                    record = ReportRecord.objects.get(agent=agent, spoof_agent=bad_agent)
                    status = 'Done'
                except:
                    pass
            ba = {
                'name': bad_agent.name,
                'status': status,
            }
            r['bad_agents'].append(ba)

        data['reports'].append(r)
	
    return HttpResponse(json.dumps(data))

def api_record(request, user, report):
    """Record agent report spoofagent history."""
    try:
        agent, created = Agent.objects.get_or_create(name=user)
        if created:
            agent.save()
        spoof_agent = SpoofAgent.objects.filter(name=report)
        report_record = ReportRecord(agent=agent, spoof_agent=spoof_agent[0])
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
        
        bad_agents = request.POST.get('bad_agents').split(',')
        for bad_agent_name in bad_agents:
            bad_agent, is_create = SpoofAgent.objects.get_or_create(name=bad_agent_name.strip(),
                                                                    report=report)
            bad_agent.save()

        return redirect('reports:admin_page')
    return HttpResponse(status=404)

def get_file(request):
    pass
    
