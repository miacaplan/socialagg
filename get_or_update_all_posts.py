from pprint import pprint
import facebook
import models

with open('TOKEN.txt') as rin:
    TOKEN = rin.read()

graph = facebook.GraphAPI(access_token=TOKEN,version='2.5')
for page in models.pages_collection.find():
    if not page.get('username'):
        continue
    print('Updating page "{}"'.format(page['name']))
    o = graph.get_object(page['username'] + '/posts', limit=100, order='reverse_chronological')
    for post in o['data']:
        post['page_id'] = page['id']
    res = models.upsert(models.posts_collection, o['data'])
    print('Inserted {} posts, updated {} posts.'.format(res['inserted'], res['updated']))









