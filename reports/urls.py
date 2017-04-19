from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views


app_name = 'reports'
urlpatterns = [
    url(r'^v1/$', views.index, name='index'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^v1/list', views.list, name='list'),
] + static('/v1' + settings.STATIC_URL, document_root=app_name + settings.STATIC_ROOT) \
+ static('/v1/files/', document_root=app_name + '/files/')

