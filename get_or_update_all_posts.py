from pprint import pprint
import facebook
import pymongo


client = pymongo.MongoClient()
db = client.get_database('socialagg')
pages = db.get_collection('pages')
posts = db.get_collection('posts')


