from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout

from . import views
from . import api

app_name = 'reports'
urlpatterns = [
    url(r'^v1/$', views.home, name='home_page'),
    url(r'^v1/login$', login, {'template_name': 'login.html'}, name='login_page'),
    url(r'^v1/logout$', logout, name='logout_page'),
    url(r'^v1/cheaters$', views.cheaters, name='cheaters_page'),
    url(r'^v1/reports$', views.reports, name='reports_page'),
    url(r'^v1/users$', views.users, name='users_page'),
    url(r'^v1/manage/report/(?P<r_id>[0-9]*)$', views.report_manage, name='report_manage_page'),

    url(r'^v1/api/user_list$', api.user_list, name='user_list'),
    url(r'^v1/api/cheater_list$', api.cheater_list, name='cheater_list'),
    url(r'^v1/api/report_list$', api.report_list, name='report_list'),
    url(r'^v1/api/report_list/(?P<user>[^/]+)$', api.agent_report_list, name='agent_report_list'),
    url(r'^v1/api/record/(?P<agent_name>[^/]+)/(?P<report_id>[0-9]+)/(?P<cheater_name>[a-zA-Z0-9]+)$', api.record, name='record'),
    url(r'^v1/api/savereport$', api.save_report, name='save_report'),
    url(r'^v1/api/updateagent$', api.update_agent, name='update_agent'),
    url(r'^v1/api/extension_version$', api.extension_version, name='extension_version'),
]

