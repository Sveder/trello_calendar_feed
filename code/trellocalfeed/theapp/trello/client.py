from httplib2 import Http
from urllib import urlencode
import json
import oauth2 as oauth
import time
import urlparse
import random
import os


class ResourceUnavailable(Exception):
	"""Exception representing a failed request to a resource"""

	def __init__(self, msg):
		Exception.__init__(self, "Resource unavailable: %s" % msg)
		

class Trello(object):

	def __init__(self, api_key, token, api_secret = None, token_secret = None):
		"""
		:api_key: API key generated at https://trello.com/1/appKey/generate
		:oauth_token: OAuth token generated at h
		"""

		if api_key and api_secret and token and token_secret:
			# oauth
			self.oauth_consumer = oauth.Consumer(key = api_key, secret = api_secret)
			self.oauth_token = oauth.Token(key = token, secret = token_secret)
			self.client = oauth.Client(self.oauth_consumer, self.oauth_token)

		elif api_key and token:
			self.client = Http()

		self.api_key = api_key
		self.auth_token = token
		self.api_secret = api_secret
		self.token_secret = token_secret
		

	def logout(self):
		"""Log out of Trello. This method is idempotent."""

		# TODO: refactor
		pass
		#if not self._cookie:
			#return

		#headers = {'Cookie': self._cookie, 'Accept': 'application/json'}
		#response, content = self.client.request(
				#'https://trello.com/logout',
				#'GET',
				#headers = headers,
				#)

		## TODO: error checking
		#self._cookie = None

	def build_url(self, path, query = {}):
		"""
		Builds a Trello URL.

		:path: URL path
		:params: dict of key-value pairs for the query string
		"""
		url = 'https://api.trello.com/1'
		if path[0:1] != '/':
			url += '/'
		url += path
		if hasattr(self, 'oauth_token'):
			url += '?'
			url += "key="+self.oauth_token.key
			url += "&token="+self.oauth_consumer.key
		else:
			url += '?'
			url += "key=" + self.api_key
			url += "&token=" + self.auth_token
		
		if len(query) > 0:
			url += '&'+urlencode(query)

		return url

	def list_boards(self):
		"""
		Returns all boards for your Trello user

		:return: a list of Python objects representing the Trello boards. Each board has the 
		following noteworthy attributes:
			- id: the board's identifier
			- name: Name of the board
			- desc: Description of the board
			- closed: Boolean representing whether this board is closed or not
			- url: URL to the board
		"""
		headers = {'Accept': 'application/json'}
		url = self.build_url("/members/me/boards/all")
		response, content = self.client.request(url, 'GET', headers = headers)

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)
		boards = list()
		for b in json_obj:
			board = Board(self, b['id'])
			board.name = b['name']
			board.description = b.get('desc', "No Description")
			board.closed = b['closed']
			board.url = b['url']
			boards.append(board)

		return boards


class Board(object):
	"""Class representing a Trello board. Board attributes are stored as normal Python attributes;
	access to all sub-objects, however, is always an API call (Lists, Cards).
	"""

	def __init__(self, trello, board_id):
		"""Constructor.
		
		:trello: Reference to a Trello object
		:board_id: ID for the board
		"""
		self.trello = trello
		self.id = board_id

	def fetch(self):
		"""Fetch all attributes for this board"""
		headers = {'Accept': 'application/json'}
		url = self.trello.build_url('/boards/'+self.id)
		response, content = self.trello.client.request(url, 'GET', headers = headers)

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)
		self.name = json_obj['name']
		self.description = json_obj['desc']
		self.closed = json_obj['closed']
		self.url = json_obj['url']
		
	def all_lists(self):
		"""Returns all lists on this board"""
		return self.get_lists('all')

	def open_lists(self):
		"""Returns all open lists on this board"""
		return self.get_lists('open')

	def closed_lists(self):
		"""Returns all closed lists on this board"""
		return self.get_lists('closed')

	def get_lists(self, filter):

		headers = {'Accept': 'application/json'}
		url = self.trello.build_url(
				'/boards/'+self.id+'/lists',
				{'cards': 'none', 'filter': filter})
		response, content = self.trello.client.request(url, 'GET', headers = headers)

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)
		lists = list()
		for obj in json_obj:
			l = List(self, obj['id'])
			l.name = obj['name']
			l.closed = obj['closed']
			lists.append(l)

		return lists
		
	def list_cards(self, fields=""):
		headers = {'Accept': 'application/json'}
		url = self.trello.build_url(
				'/boards/'+self.id+'/cards')
		response, content = self.trello.client.request(url, 'GET', headers = headers)

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)
		cards = list()
		for c in json_obj:
			card = Card(self, c['id'])
			card.name = c['name']
			card.description = c.get('desc', "")
			card.url = c.get('url', "")
			card.due = c.get('due', None)
			card.assignees = c.get("idMembers", [])
			card.json_obj = c
			cards.append(card)

		return cards

class List(object):
	"""Class representing a Trello list. List attributes are stored on the object, but access to 
	sub-objects (Cards) require an API call"""

	def __init__(self, board, list_id):
		"""Constructor

		:board: reference to the parent board
		:list_id: ID for this list
		"""
		self.board = board
		self.id = list_id

	def fetch(self):
		"""Fetch all attributes for this list"""
		headers = {'Accept': 'application/json'}
		url = self.board.trello.build_url('/lists/'+self.id)
		response, content = self.board.trello.client.request(url, 'GET', headers = headers)

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)
		self.name = json_obj['name']
		self.closed = json_obj['closed']

	def list_cards(self):
		headers = {'Accept': 'application/json'}
		url = self.board.trello.build_url('/lists/'+self.id+'/cards')
		response, content = self.board.trello.client.request(url, 'GET', headers = headers)

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)
		cards = list()
		for c in json_obj:
			card = Card(self, c['id'])
			card.name = c['name']
			card.description = c['desc']
			card.closed = c['closed']
			card.url = c['url']
			card.due = c.get('due', None)
			cards.append(card)

		return cards

	def add_card(self, name, desc = None):
		"""Add a card to this list

		:name: name for the card
		:return: the card
		"""
		headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
		url = self.board.trello.build_url('/lists/'+self.id+'/cards')
		request = {'name': name, 'idList': self.id, 'desc': desc}
		response, content = self.board.trello.client.request(
				url,
				'POST',
				headers = headers,
				body = json.dumps(request))

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)
		card = Card(self, json_obj['id'])
		card.name = json_obj['name']
		card.description = json_obj['desc']
		card.closed = json_obj['closed']
		card.url = json_obj['url']
		return card

class Card(object):
	""" Class representing a Trello card. Card attributes are stored on the object"""

	def __init__(self, trello_board, card_id):
		"""Constructor

		:trello_list: reference to the parent list
		:card_id: ID for this card
		"""
		self.board = trello_board
		self.id = card_id

	def fetch(self):
		"""Fetch all attributes for this card"""
		headers = {'Accept': 'application/json'}
		url = self.board.trello.build_url('/cards/'+self.id, {'badges': False})
		response, content = self.board.trello.client.request(url, 'GET', headers = headers)

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)

		self.name = json_obj['name']
		self.description = json_obj['desc']
		self.closed = json_obj['closed']
		self.url = json_obj['url']
		self.due = json_obj.get("due", None)
