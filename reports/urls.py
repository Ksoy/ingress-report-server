from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout

from . import views


app_name = 'reports'
urlpatterns = [
    url(r'^v1/$', views.home_page, name='home_page'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^v1/list$', views.list_page, name='list_page'),
    url(r'^v1/manage$', views.manage_page, name='manage_page'),
    url(r'^v1/login$', login, {'template_name': 'login.html'}, name='login_page'),
    url(r'^v1/logout$', logout, name='logout_page'),

    url(r'^v1/api/list/(?P<user>[a-zA-Z0-9]+)$', views.api_list, name='list'),
    url(r'^v1/api/record/(?P<user>[a-zA-Z0-9]+)/(?P<report>[a-zA-Z0-9]+)$', views.api_record, name='record'),
] + static('/v1' + settings.STATIC_URL, document_root=app_name + settings.STATIC_ROOT) \
+ static('/v1/files/', document_root=app_name + '/files/')

