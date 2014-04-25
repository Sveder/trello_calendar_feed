from client import Trello
import unittest
import os

#The api and secret for the "PyTrello Test User"
TRELLO_API_KEY = r"8410de3ae39c4a63086afb888560d5bd"
TRELLO_OAUTH_SECRET = r"21f56da9cabaefdc34aeec9f62ffeda0d5c1bb6548e3ac99460e9119bf3bbedf"

class TrelloTestCase(unittest.TestCase):
	"""
	Tests for Trello API. Note these test are in order to preserve dependencies, as an API 
	integration cannot be tested independently.
	
	Sveder: Eventually the test will be self encompasing (meaning on set up you
	build the board, organization and whatever up) and then access it using the
	api. For now, I'm converting it to use the public board:
	https://trello.com/board/pytrello-test-board/4f80ca3a48bc86b25333becb
	"""
	
	def setUp(self):
		self.trello = Trello(TRELLO_API_KEY, TRELLO_OAUTH_SECRET)
	
	def tearDown(self):
		#self._trello.logout()
		pass

	def test_01_list_boards(self):

		board_count = self.trello.list_boards()
		print board_count
		#self.assertEquals(
		#		len(self._trello.list_boards()),
		#		int(os.environ['TRELLO_TEST_BOARD_COUNT']))

	#def test10_board_attrs(self):
	#	boards = self._trello.list_boards()
	#	for b in boards:
	#		self.assertIsNotNone(b.id, msg="id not provided")
	#		self.assertIsNotNone(b.name, msg="name not provided")
	#		self.assertIsNotNone(b.description, msg="description not provided")
	#		self.assertIsNotNone(b.closed, msg="closed not provided")
	#		self.assertIsNotNone(b.url, msg="url not provided")
	#
	#def test20_board_all_lists(self):
	#	boards = self._trello.list_boards()
	#	for b in boards:
	#		try:
	#			b.all_lists()
	#		except Exception as e:
	#			self.fail("Caught Exception getting lists")
	#
	#def test21_board_open_lists(self):
	#	boards = self._trello.list_boards()
	#	for b in boards:
	#		try:
	#			b.open_lists()
	#		except Exception as e:
	#			self.fail("Caught Exception getting open lists")
	#
	#def test22_board_closed_lists(self):
	#	boards = self._trello.list_boards()
	#	for b in boards:
	#		try:
	#			b.closed_lists()
	#		except Exception as e:
	#			self.fail("Caught Exception getting closed lists")
	#
	#def test30_list_attrs(self):
	#	boards = self._trello.list_boards()
	#	for b in boards:
	#		for l in b.all_lists():
	#			self.assertIsNotNone(l.id, msg="id not provided")
	#			self.assertIsNotNone(l.name, msg="name not provided")
	#			self.assertIsNotNone(l.closed, msg="closed not provided")
	#		break # only need to test one board's lists
	#
	#def test40_list_cards(self):
	#	boards = self._trello.list_boards()
	#	for b in boards:
	#		for l in b.all_lists():
	#			for c in l.list_cards():
	#				self.assertIsNotNone(c.id, msg="id not provided")
	#				self.assertIsNotNone(c.name, msg="name not provided")
	#				self.assertIsNotNone(c.description, msg="description not provided")
	#				self.assertIsNotNone(c.closed, msg="closed not provided")
	#				self.assertIsNotNone(c.url, msg="url not provided")
	#			break
	#		break
	#	pass
	#
	#def test50_add_card(self):
	#	boards = self._trello.list_boards()
	#	board_id = None
	#	for b in boards:
	#		if b.name != os.environ['TRELLO_TEST_BOARD_NAME']:
	#			continue
	#
	#		for l in b.open_lists():
	#			try:
	#				name = "Testing from Python - no desc"
	#				card = l.add_card(name)
	#			except Exception as e:
	#				print str(e)
	#				self.fail("Caught Exception adding card")
	#
	#			self.assertIsNotNone(card, msg="card is None")
	#			self.assertIsNotNone(card.id, msg="id not provided")
	#			self.assertEquals(card.name, name)
	#			self.assertIsNotNone(card.closed, msg="closed not provided")
	#			self.assertIsNotNone(card.url, msg="url not provided")
	#			break
	#		break
	#	if not card:
	#		self.fail("No card created")
	#
	#def test51_add_card(self):
	#	boards = self._trello.list_boards()
	#	board_id = None
	#	for b in boards:
	#		if b.name != os.environ['TRELLO_TEST_BOARD_NAME']:
	#			continue
	#
	#		for l in b.open_lists():
	#			try:
	#				name = "Testing from Python"
	#				description = "Description goes here"
	#				card = l.add_card(name, description)
	#			except Exception as e:
	#				print str(e)
	#				self.fail("Caught Exception adding card")
	#
	#			self.assertIsNotNone(card, msg="card is None")
	#			self.assertIsNotNone(card.id, msg="id not provided")
	#			self.assertEquals(card.name, name)
	#			self.assertEquals(card.description, description)
	#			self.assertIsNotNone(card.closed, msg="closed not provided")
	#			self.assertIsNotNone(card.url, msg="url not provided")
	#			break
	#		break
	#	if not card:
	#		self.fail("No card created")


if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TrelloTestCase)
	unittest.TextTestRunner(verbosity=2).run(suite)
