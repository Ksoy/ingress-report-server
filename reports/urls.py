from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout

from . import views
from . import api

app_name = 'reports'
urlpatterns = [
    url(r'^v1/$', views.home_page, name='home_page'),
    url(r'^v1/login$', login, {'template_name': 'login.html'}, name='login_page'),
    url(r'^v1/logout$', logout, name='logout_page'),
    url(r'^v1/list$', views.list_page, name='list_page'),
    url(r'^v1/info/(?P<r_id>[0-9]*)$', views.info_page, name='info_page'),
    url(r'^v1/manage_report$', views.manage_report_page, name='manage_report_page'),
    url(r'^v1/manage_user$', views.manage_user_page, name='manage_user_page'),
    url(r'^v1/manage/(?P<r_id>[0-9]*)$', views.edit_report_page, name='manage_page'),

    url(r'^v1/api/list/(?P<user>[a-zA-Z0-9]+)$', api.list, name='list'),
    url(r'^v1/api/record/(?P<agent_name>[a-zA-Z0-9]+)/(?P<report_id>[0-9]+)/(?P<cheater_name>[a-zA-Z0-9]+)$', api.record, name='record'),
    url(r'^v1/api/savereport$', api.save_report, name='save_report'),
    url(r'^v1/api/updateagent$', api.update_agent, name='update_agent'),
    url(r'^v1/api/extension_version$', api.extension_version, name='extension_version'),
]

