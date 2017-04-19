import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import SpoofAgent, Report

# Create your views here.
def index(request):
    return render(request, 'index.html') # HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

######################################################################

def admin(request):
    """Report management page."""
    pass

def list(request):
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
            'file_link': '/reports/files/{}'.format(report.report_file.name),
        }
        for bad_agent in SpoofAgent.objects.filter(report=report):
            r['bad_agents'].append(bad_agent.name)

        data['reports'].append(r)

    print(data)
	
    return HttpResponse(json.dumps(data))

def list_page(request):
    """List all reports page."""

    spoof_agent_list = SpoofAgent.objects.all()
    data = serializers.serialize("json", SpoofAgent.objects.filter(report_id=1))
    print(data)
    context = {
        'spoof_agent_list': spoof_agent_list,
    }
    
    return render(request, 'list.html', context)

def record(request):
    """Record agent report spoofagent history."""
    pass

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

