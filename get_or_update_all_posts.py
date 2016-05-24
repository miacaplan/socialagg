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
    o = graph.get_object(page['username'] + '/posts', fields='id,created_time,shares,status_type,likes.summary(true)',limit=100, order='reverse_chronological')
    for post in o['data']:
        post['page_id'] = page['id']
        post['likes'] = post.get('likes', {}).get('summary', {}).get('total_count', 0)
        post['shares'] = post.get('shares', {}).get('count', 0)
    res = models.upsert(models.posts_collection, o['data'])
    print('Inserted {} posts, updated {} posts.'.format(res['inserted'], res['updated']))









