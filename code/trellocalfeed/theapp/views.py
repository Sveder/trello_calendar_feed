import django.shortcuts as shortcuts
from django.http import HttpResponse

import logic
import models


def home(request):
    return shortcuts.render_to_response("index.html")

def user_page(request, url):
    """
    Generate a user page that contains the form to create a new feed and the collection of all previous feeds.
    """
    try:
        user_model = models.FeedUser.objects.get(url=url)
    except:
        return shortcuts.redirect("/trello?error=2")
    
    #TODO: Save longlived cookie
    
    feeds = models.Feed.objects.filter(feed_user=user_model)
    boards = logic.get_all_board_names(user_model.user_token)
    
    
    return shortcuts.render(request, "user_page.html", {"user" : user_model, "feeds" : feeds, "boards" : boards})

def feed(request, url):
    try:
        feed_model = models.Feed.objects.get(url=url)
    except models.Feed.DoesNotExist:
        return shortcuts.redirect("/trello?error=1")
        
    calendar = logic.create_calendar_from_feed(feed_model)
    ical_feed = calendar.to_ical()
    
    return HttpResponse(ical_feed, content_type="text/calendar")