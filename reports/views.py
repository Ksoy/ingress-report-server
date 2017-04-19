import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from .models import SpoofAgent, Report, ReportRecord, Agent

# Create your views here.
def home_page(request):
    return render(request, 'home.html') # HttpResponse("Hello, world. You're at the polls index.")

@login_required(login_url='/reports/v1/login')
def manage_page(request):
    """Report management page."""
    return render(request, 'manage.html')

def api_list(request):
    """Reutn all report information."""
    data = {
        'reports': []
    }
    for report in Report.objects.all():
        r = {
            'subject': report.subject,
            'description': report.description,
            'bad_agents': [],
            'inappropriate_type': report.inappropriate_type,
            'file_link': '/reports/v1/files/{}.zip'.format(report.report_file.name),
        }
        for bad_agent in SpoofAgent.objects.filter(report=report):
            ba = {
                'name': bad_agent.name,
                'status': bad_agent.status,
            }
            r['bad_agents'].append(ba)

        data['reports'].append(r)
	
    return HttpResponse(json.dumps(data))

def list_page(request):
    """List all reports page."""

    spoof_agent_list = SpoofAgent.objects.all()
    #data = serializers.serialize("json", SpoofAgent.objects.filter(report_id=1))
    context = {
        'bad_agent_list': spoof_agent_list,
    }
    
    return render(request, 'list.html', context)


def api_record(request, user, report):
    """Record agent report spoofagent history."""
    try:
        agent = Agent.objects.filter(name=user)
        spoof_agent = SpoofAgent.objects.filter(name=report)
        report_record = ReportRecord(agent=agent[0], spoof_agent=spoof_agent[0])
        report_record.save()
    except:
        return HttpResponse('false')

    return HttpResponse('ok')

def create_report(request):
    """Create new report by admin."""
    pass

def update_report(request):
    """Update report by admin"""
    pass

def upload(request):
    """Upload report file."""
    pass

def download(request, file_name):
    """Download report file."""
    pass

