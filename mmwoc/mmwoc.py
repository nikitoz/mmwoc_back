from twisted.web import server, resource
from twisted.internet import reactor, defer
import pymongo
from twisted.python import log
import json

class mmwoc(resource.Resource):
	isLeaf = True

	def __init__(self):
		self.try_auth()

	def try_auth(self):
		self.authed = False
		try:
			self.client = pymongo.MongoClient('mongodb://localhost:27017/')
			self.authed = self.client['mmwocdb'].authenticate('public', 'public')
		except pymongo.errors.PyMongoError as e:
			pass
		return self.authed

	def isAuthed(self):
		if (self.authed == False) :
			self.try_auth()
		return self.authed

	def answer(self, request, result):
		request.setHeader("content-type", "application/json")
		if ('data' not in result or request.args is None or 'callback' not in request.args):
			return
		sr = json.dumps(result[u'data'], ensure_ascii=False).encode('utf-8')
		request.write(request.args['callback'][0] + "(" + sr + ")")
		return ''
	
	def render_GET(self, request):
		if (not self.isAuthed() or '_id' not in request.args):
			return self.answer(request, {u'data' : {}})
		res = {}			
		try:
			res = self.client['mmwocdb'].graph.find_one({"_id" : request.args['_id'][0]})
		except pymongo.errors.PyMongoError as e:
			print str(e)
			pass
		return self.answer(request, res)

	def getChild(self, name, request):
		pass
