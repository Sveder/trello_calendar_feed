import django.shortcuts as shortcuts
from django.http import HttpResponse

import logic
import models

def _get_user_from_request(request):
    """
    Return a user model from the request. There are basically two options:
    1. the "cur_user" is an integer, meaning the code is updated and just return
       the correct model.
    2. the "cur_user" is a model, which means you need to convert it to a user_id
       in the session cookie and then return the correct model. 
    """
    cur_user_from_session = request.session["cur_user"]
    
    if type(cur_user_from_session) is int:
        user_model = models.FeedUser.objects.get(id=cur_user_from_session)
    else:
        request.session["cur_user"] = cur_user_from_session.id
        user_model = cur_user_from_session
        
    return user_model

def redirect_to_sveder(request):
    return shortcuts.redirect("http://sveder.com")

def faq(request):
    return shortcuts.render_to_response("faq.html")

def home(request):
    if "cur_user" in request.session:
        user = _get_user_from_request(request)
        return shortcuts.redirect("/user/%s" % user.url)
    
    return shortcuts.render_to_response("index.html")

def user_page(request, url):
    """
    Generate a user page that contains the form to create a new feed and the collection of all previous feeds.
    """
    try:
        user_model = models.FeedUser.objects.get(url=url, is_valid=True)
    except:
        return shortcuts.redirect("/trello?error=2")
    
    #TODO: Save longlived cookie
    request.session["cur_user"] = user_model.id
    
    
    feeds = models.Feed.objects.filter(feed_user=user_model)
    boards = logic.get_all_boards(user_model.user_token)
    
    return shortcuts.render(request, "user_page.html", {"user" : user_model, "feeds" : feeds, "boards" : boards})

def feed(request, url):
    try:
        feed_model = models.Feed.objects.get(url=url, is_valid=True)
    except models.Feed.DoesNotExist:
        return shortcuts.redirect("/trello?error=1")
    
    #There are some old feeds around that have no user attacehd to them, and so I can't get
    #their token and actually create the feed, so I check this now and redirect instead
    #of crashing. Reported by Sentry.
    try:
        feed_model.feed_user
    except models.FeedUser.DoesNotExist:
        return shortcuts.redirect("/trello?error=2")
        
    calendar = logic.create_calendar_from_feed(feed_model)
    ical_feed = calendar.to_ical()
    
    content_type = "text/calendar"
    if "debug" in request.REQUEST:
        content_type="text/plain"
        
    content_type += "; charset=utf-8"
    
    return HttpResponse(ical_feed, content_type=content_type)
