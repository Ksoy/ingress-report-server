from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout

from . import views


app_name = 'reports'
urlpatterns = [
    url(r'^v1/$', views.home_page, name='home_page'),
    url(r'^v1/login$', login, {'template_name': 'login.html'}, name='login_page'),
    url(r'^v1/logout$', logout, name='logout_page'),
    url(r'^v1/list$', views.list_page, name='list_page'),
    url(r'^v1/admin$', views.admin_page, name='admin_page'),
    url(r'^v1/manage/(?P<r_id>[0-9]*)$', views.manage_page, name='manage_page'),

    url(r'^v1/api/list/(?P<user>[a-zA-Z0-9]+)$', views.api_list, name='list'),
    url(r'^v1/api/record/(?P<user>[a-zA-Z0-9]+)/(?P<report>[a-zA-Z0-9]+)$', views.api_record, name='record'),
    url(r'^v1/api/savereport$', views.api_save_report, name='save_report'),
    url(r'^v1/api/updateagent$', views.api_update_agent, name='update_agent'),
]

