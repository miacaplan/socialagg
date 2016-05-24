import concurrent
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
import facebook

import connect
import models
import dateutil.parser


def upsert_page_posts(page):
    print('Updating page "{}"'.format(page['name']))
    o = connect.get_fb_graph().get_object(page['username'] + '/posts',
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


with ThreadPoolExecutor() as executor:
    future_to_page_id = {executor.submit(upsert_page_posts, page): page['id'] for page in
                         models.pages_collection.find()}
    for future in concurrent.futures.as_completed(future_to_page_id):
        page_id = future_to_page_id[future]
        try:
            data = future.result()
        except Exception as exc:
            print('page id %r generated an exception: %s' % (page_id, exc))
        else:
            print('page id {} succeeded'.format(page_id))
