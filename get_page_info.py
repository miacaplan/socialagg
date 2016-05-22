from pprint import pprint
import facebook
import pymongo
import sys
import os


with open('TOKEN.txt') as rin:
    TOKEN = rin.read()

# FOLLOWING = ['HillaryClinton', 'DonaldTrump', 'BernieSanders']

def get_page_info(name):
    graph = facebook.GraphAPI(access_token=TOKEN,version='2.5')
    client = pymongo.MongoClient()
    db = client.get_database('socialagg')
    pages = db.get_collection('pages')

    pc = pages.find({'username':name})
    if pc and pc.count() > 0:
        return pc[0]


    o = graph.get_object(name, fields="id,about,name,website,username,fan_count")
    pages.update({'id':o['id']}, {k:v for k,v in o.items()}, upsert=True)
    return pages.find({'username':name})[0]


if __name__ == '__main__':
    USAGE = 'USAGE: {} page_url'.format(os.path.basename(sys.argv[0]))
    if len(sys.argv) != 2:
        pprint(USAGE)
        exit(1)

    new_name = os.path.basename(sys.argv[1].strip('/'))
    try:
        added = get_page_info(new_name)
        pprint("OK, added id #{} with {} fans.".format(added['id'], added['fan_count']))
    except facebook.GraphAPIError:
        print("Not a page")



# db.create_collection('pages')
# pages.drop()
# for p in pages.find():
#     pprint(p)

# URL = "https://graph.facebook.com/oauth/access_token"

# graph = facebook.GraphAPI(access_token=TOKEN, varsion='2.5')
