import urlparse
import oauth2 as oauth
import re
from datetime import datetime
from icalendar import Calendar, Event
import time
import random

from trello import client as Client

##API_KEY = r"9cf5a88e6a3a9897d59e55bfc327b5d5"
##OAUTH_KEY = r"c6ae666b92a0a6d3e04b1fd2bd48f462aed588e032e82642a2eac32e026aa1f7"
##
##z = """
##REQUEST = r"https://trello.com/1/OAuthGetRequestToken"
###https://trello.com/1/OAuthAuthorizeToken
###https://trello.com/1/OAuthGetAccessToken
##
##consumer_key = r"9cf5a88e6a3a9897d59e55bfc327b5d5"
##consumer_secret = r"c6ae666b92a0a6d3e04b1fd2bd48f462aed588e032e82642a2eac32e026aa1f7"
##
##request_token_url = r"https://trello.com/1/OAuthGetRequestToken"
##access_token_url = r"https://trello.com/1/OAuthGetAccessToken"
##authorize_url = r'https://trello.com/1/OAuthAuthorizeToken'
##
##consumer = oauth.Consumer(consumer_key, consumer_secret)
##client = oauth.Client(consumer)
##
### Step 1: Get a request token. This is a temporary token that is used for 
### having the user authorize an access token and to sign the request to obtain 
### said access token.
##
##resp, content = client.request(request_token_url, "GET")
##if resp['status'] != '200':
##    raise Exception("Invalid response %s." % resp['status'])
##
##request_token = dict(urlparse.parse_qsl(content))
##
##print "Request Token:"
##print "    - oauth_token        = %s" % request_token['oauth_token']
##print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
##print 
##
### Step 2: Redirect to the provider. Since this is a CLI script we do not 
### redirect. In a web application you would redirect the user to the URL
### below.
##
##print "Go to the following link in your browser:"
##print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
##print 
##
### After the user has granted access to you, the consumer, the provider will
### redirect you to whatever URL you have told them to redirect to. You can 
### usually define this in the oauth_callback argument as well.
##accepted = 'n'
##while accepted.lower() == 'n':
##    accepted = raw_input('Have you authorized me? (y/n) ')
##oauth_verifier = raw_input('What is the PIN? ')
##
### Step 3: Once the consumer has redirected the user back to the oauth_callback
### URL you can request the access token the user has approved. You use the 
### request token to sign this request. After this is done you throw away the
### request token and use the access token returned. You should store this 
### access token somewhere safe, like a database, for future use.
##token = oauth.Token(request_token['oauth_token'],
##    request_token['oauth_token_secret'])
##token.set_verifier(oauth_verifier)
##client = oauth.Client(consumer, token)
##
##resp, content = client.request(access_token_url, "POST")
##access_token = dict(urlparse.parse_qsl(content))
##
##print "Access Token:"
##print "    - oauth_token        = %s" % access_token['oauth_token']
##print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
##print
##print "You may now access protected resources using the access tokens above." 
##print
##"""
##oauth_token = r"45eb0357e108939e60087ea921260d67f21f7f758b0a63e2e4e6c00b2dbf7a7c"
##oauth_token_secret = r"853fffeb98b091d2e1b4eec8f7a239a7"
##
##due_date_cards = []
##
##t = Client.Trello(API_KEY, OAUTH_KEY, oauth_token, oauth_token_secret)
##boards = t.list_boards()
##for board in boards:
###	if board.name == "test":
##	cards = []
##	for list in board.all_lists():
##		cards += list.list_cards()
##		
##	for card in cards:
##		card.fetch()
##		if card.due != None:
##			due_date_cards.append(card)
##
##cal = Calendar()
##cal.add('version', '2.0')
##
##for i in due_date_cards:
##	start = datetime.strptime(i.due, "%Y-%m-%dT%H:%M:%S.%fZ")
##
##
##	event = Event()
##	event.add('summary', i.name)
##	event.add('DESCRIPTION', i.url)
##	event.add('dtstart', start)
##	event.add('dtend', start)
##	event.add('dtstamp', start)
##	event['uid'] = str(time.time()) + str(random.random())
##	event.add('priority', 5)
##	
##	cal.add_component(event)
##
##print dir(cal)
##print cal.to_ical()	
##f = open('example.ics', 'wb')
##f.write(cal.to_ical())
##f.close()
##

API_KEY = r"9cf5a88e6a3a9897d59e55bfc327b5d5"
user_token = r"a104756a5224894c5a27efa16b512213bbd60ab54bf6b03b15f75fe213a9f2f9"

due_date_cards = []

t = Client.Trello(API_KEY, user_token)
boards = t.list_boards()
b_count = 0
c_count = 0
for board in boards:
	b_count += 1
	cards = board.list_cards("due")
	c_count += len(cards)
	for card in cards:
		if card.due != None:
			due_date_cards.append(card)

print b_count, "boards"
print c_count, "cards"