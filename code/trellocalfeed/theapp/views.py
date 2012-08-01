import django.shortcuts as shortcuts
from django.http import HttpResponse

import logic
import models


def home(request):
    return shortcuts.render_to_response("index.html")

def feed(request, url):
    try:
        feed_model = models.Feed.objects.get(url=url)
    except models.Feed.DoesNotExist:
        return shortcuts.redirect("/")
        
    calendar = logic.create_calendar_from_feed(feed_model)
    ical_feed = calendar.to_ical()
    print ical_feed
    
    return HttpResponse(ical_feed, content_type="text/calendar")