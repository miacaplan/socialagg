from pprint import pprint
import facebook

import connect
import models
import dateutil.parser

# with open('TOKEN.txt') as rin:
#     TOKEN = rin.read()


for page in models.pages_collection.find():
    if not page.get('username'):
        continue
    print('Updating page "{}"'.format(page['name']))
    o = connect.graph.get_object(page['username'] + '/posts',
                                 fields='id,created_time,shares,status_type,likes.summary(true), updated_time, message, from',
                                 limit=100, order='reverse_chronological')
    for post in o['data']:
        post['page_id'] = page['id']
        post['likes'] = post.get('likes', {}).get('summary', {}).get('total_count', 0)
        post['shares'] = post.get('shares', {}).get('count', 0)
        post['created_time'] = dateutil.parser.parse(post['created_time'])
        post['updated_time'] = dateutil.parser.parse(post['updated_time'])
    res = models.upsert(models.posts_collection, o['data'])
    print('Inserted {} posts, updated {} posts.'.format(res['inserted'], res['updated']))
