from bottle import route, run, template
from pprint import pprint

import pymongo

client = pymongo.MongoClient()
db = client.get_database('socialagg')
pages = db.get_collection('pages')

CANDIDATE_LIST_ITEM = '''<li>
    <a href="/{id}">{name}</a>
</li>
'''

@route('/index')
def index():
    candidates_str = ""
    for p in pages.find():
        # pprint(p)
        candidates_str+=CANDIDATE_LIST_ITEM.format(**p)

    # pprint(candidates_str)
    with open("index_template.html") as index:
        candidates_template=index.read().format(candidates_str)

    return template(candidates_template)
    # return template('<b>Hello {{name}}</b>!', name=name)

@route('/<id>')
def index(id):
    with open('item_template.html') as tempin:
        page_str = tempin.read()

    for p in pages.find({'id':id}):
        page_str  = page_str.format(**p)
        # pprint(p)
        break
        # candidates_str+=CANDIDATE_LIST_ITEM.format(**p)

    # pprint(candidates_str)
    # with open("index_template.html") as index:
    #     candidates_template=index.read().format(candidates_str)

    return template(page_str)  #template(candidates_template)
    # return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)