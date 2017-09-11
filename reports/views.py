import json
import os
import ntpath

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect#, render
from django.template import loader

from .render import render
from .models import Agent, Cheater, Report, ReportCheater
from .config import INAPPROPRIATE_MAP, REPORT_STATUS_LIST

def home(request):
    burns = len(Cheater.objects.filter(status='burned'))
    return render(request, 'home.html', {'burns': burns}) 

def cheaters(request):
    return render(request, 'cheater_list.html')

@login_required(login_url='/reports/v1/login')
def reports(request):
    return render(request, 'report_list.html')

@login_required(login_url='/reports/v1/login')
def agents(request):
    return render(request, 'agent_list.html')

@login_required(login_url='/reports/v1/login')
def users(request):
    return render(request, 'user_list.html')

@login_required(login_url='/reports/v1/login')
def user_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_superuser(username=username, password=password, email='')
        return redirect('reports:users_page')
    return render(request, 'user_create.html')

@login_required(login_url='/reports/v1/login')
def user_manage(request, user_id):
    if int(user_id) != int(request.user.id):
        return redirect('reports:home_page')

    if request.method == 'POST':
        user_id = request.POST['id']
        user_name = request.POST['username']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        new_password_c = request.POST['new_password_c']

        if new_password != new_password_c:
            return render(request, 'user_profile.html', {'error': 'New password not match.'})

        try:
            user = User.objects.get(id=user_id, username=user_name)
        except:
            return render(request, 'user_profile.html', {'error': 'User not find.'})

        if not user.check_password(old_password):
            return render(request, 'user_profile.html', {'error': 'Wrong password.'})

        user.set_password(new_password)
        user.save()
        return render(request, 'user_profile.html', {'success': True})

    return render(request, 'user_profile.html')

@login_required(login_url='/reports/v1/login')
def agent_manage(request, a_id=None):
    context = {
        'agent': { 'is_reliable': False},
    }
    if a_id:
        context['agent'] = Agent.objects.get(id=a_id)
    return render(request, 'agent_manage.html', context)

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
