from pprint import pprint
import facebook
import pymongo
import sys
import os
import models
import connect


# running_dir = os.path.dirname(__file__)
# with open(os.path.join(running_dir, 'TOKEN.txt')) as rin:
#     TOKEN = rin.read()


# FOLLOWING = ['HillaryClinton', 'DonaldTrump', 'BernieSanders']

def get_page_info(name, forced_update=False):
    # print(name)
    # print("graph obj", graph.get_object())
    pc = models.pages_collection.find({'username': name})
    if (not forced_update) and pc and pc.count() > 0:
        return pc[0]

    o = connect.get_fb_graph().get_object(name, fields="id,about,name,website,username,likes, fan_count")
    o['website'] = o['website'].split()[0]  # TODO insert the list of websites and show a list of them
    # pprint('o:{0}'.format(o))
    models.pages_collection.update({'id': o['id']}, {k: v for k, v in o.items()}, upsert=True)
    return models.pages_collection.find({'username': name})[0]


if __name__ == '__main__':
    USAGE = 'USAGE: {} page_url'.format(os.path.basename(sys.argv[0]))
    if len(sys.argv) != 2:
        pprint(USAGE)
        exit(1)

    # TODO - get e=optional arg 'forced_update' from user (using arg_parse etc.)
    new_name = os.path.basename(sys.argv[1].strip('/')).strip()
    try:
        added = get_page_info(new_name, forced_update=True)
        pprint("OK, added id #{} with {} fans.".format(added['id'], added['fan_count']))
    except facebook.GraphAPIError:
        print("Not a page")



# db.create_collection('pages')
# pages.drop()
# for p in pages.find():
#     pprint(p)

# URL = "https://graph.facebook.com/oauth/access_token"

# graph = facebook.GraphAPI(access_token=TOKEN, varsion='2.5')
