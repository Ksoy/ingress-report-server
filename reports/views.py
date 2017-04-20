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

# Create your views here.
def home_page(request):
    return render(request, 'home.html') # HttpResponse("Hello, world. You're at the polls index.")

@login_required(login_url='/reports/v1/login')
def manage_page(request):
    """Report management page."""
    return render(request, 'manage.html')

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

def upload_page(request):
    return render(request, 'upload.html')


def api_list(request, user):
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
            'file_link': '/reports/v1/files/{}'.format(report.report_file.name),
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

def handle_uploaded_file(filename, upload_file):
    return
    with open('reports/{}'.format(filename), 'wb+') as destination:
        for chunk in upload_file.chunks():
            destination.write(chunk)

def api_upload(request):
    if request.method == 'POST':
        upload_file = request.FILES['upload_file']
        report_file = ReportFile(upload_file=upload_file)
        report_file.save()
        handle_uploaded_file(report_file.upload_file.name, upload_file)

    else:
        return HttpResponse(status=404)

    return HttpResponse(ntpath.basename(report_file.upload_file.name))
    

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

