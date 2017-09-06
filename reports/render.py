import re
import os

from pathlib import Path
from django.shortcuts import render as render_

user_agents_android_search_regex = re.compile(u"(?:android)", re.IGNORECASE)
user_agents_mobile_search_regex = re.compile(u"(?:mobile)", re.IGNORECASE)
user_agents_tablets_search_regex = re.compile(u"(?:ipad|tablet)", re.IGNORECASE)


def render(request, template_name, context=None, content_type=None, status=None, using=None):
    print('RENDER')
    user_agent = request.META.get('HTTP_USER_AGENT')

    if user_agents_tablets_search_regex.search(user_agent):
        # is_tablet = True
        pass
    elif (user_agents_android_search_regex.search(user_agent) and
          not user_agents_mobile_search_regex.search(user_agent)):
        # is_tablet = True
        pass
    elif user_agents_mobile_search_regex.search(user_agent):
        # is_mobile
        if Path('{}/templates/mobile/{}'.format(os.path.dirname(os.path.abspath(__file__)), template_name)).is_file():
            return render_(request, template_name, context, content_type, status, using)
        else:
            return render_(request, 'mobile/working.html', context, content_type, status, using)

    return render_(request, template_name, context, content_type, status, using)
    
