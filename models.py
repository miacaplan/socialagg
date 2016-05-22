from pprint import pprint
import pymongo

client = pymongo.MongoClient()
db = client.get_database('socialagg')
pages_collection = db.get_collection('pages')
posts_collection = db.get_collection('posts')


def upsert_pages(pages):
    num_updated = 0
    num_inserted = 0
    num_ok = 0
    for page in pages:
        res = pages_collection.update({'id': page['id']}, page, upsert=True)
        if res['ok']:
            num_ok += 1
            if res['updatedExisting']:
                num_updated += 1
            else:
                num_inserted += 1
    return {'ok': num_ok, 'updated': num_updated, 'inserted': num_inserted}

