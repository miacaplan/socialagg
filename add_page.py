from pprint import pprint
import facebook
import pymongo
import sys
import os
import models

with open('TOKEN.txt') as rin:
    TOKEN = rin.read()

# FOLLOWING = ['HillaryClinton', 'DonaldTrump', 'BernieSanders']

def get_page_info(name):
    print(name)
    graph = facebook.GraphAPI(access_token=TOKEN,version='2.5')
    # print("graph obj", graph.get_object())
    pc = models.pages_collection.find({'username':name})
    if pc and pc.count() > 0:
        return pc[0]


    o = graph.get_object(name, fields="id,about,name,website,username,likes")
    pprint('o:{0}'.format(o))
    models.pages_collection.update({'id':o['id']}, {k:v for k,v in o.items()}, upsert=True)
    return models.pages_collection.find({'username':name})[0]


if __name__ == '__main__':
    USAGE = 'USAGE: {} page_url'.format(os.path.basename(sys.argv[0]))
    if len(sys.argv) != 2:
        pprint(USAGE)
        exit(1)

    new_name = os.path.basename(sys.argv[1].strip('/')).strip()
    # try:
    added = get_page_info(new_name)
    pprint("OK, added id #{} with {} fans.".format(added['id'], added['likes']))
    # except facebook.GraphAPIError:
    #     print("Not a page")



# db.create_collection('pages')
# pages.drop()
# for p in pages.find():
#     pprint(p)

# URL = "https://graph.facebook.com/oauth/access_token"

# graph = facebook.GraphAPI(access_token=TOKEN, varsion='2.5')
