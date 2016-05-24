from bottle import route, run, template
from pprint import pprint

import pymongo

import models

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
        candidates_str += CANDIDATE_LIST_ITEM.format(**p)

    # pprint(candidates_str)
    with open("templates/index_template.html") as index:
        candidates_template = index.read().format(candidates_str)

    return template(candidates_template)
    # return template('<b>Hello {{name}}</b>!', name=name)


# show_posts.py
@route('/latest')
def latest():
    posts_list_page = "<ul>"
    # for p in models.posts_collection.find().sort({'updated_time': 1}).limit(50):
    for p in models.posts_collection.find().sort('updated_time', 1).limit(50):
        # pprint(p)
        """
        post record example:
        {'page_id': '124955570892789', '_id': ObjectId('57441554d15af3b63cef877b'), 'status_type': 'shared_story', 'likes': 3061,
         'created_time': '2016-05-24T04:55:01+0000', 'shares': 415, 'id': '124955570892789_1053722661349404'}
        """
        posts_list_page += "<li>message: {message} likes: {likes}</li>\n".format(**p)

    posts_list_page += "</ul>"

    return posts_list_page


@route('/pages/<id>')
def index(id):
    with open('templates/item_template.html') as tempin:
        page_str = tempin.read()

    for p in pages.find({'id': id}):
        page_str = page_str.format(**p)
        # pprint(p)
        break
        # candidates_str+=CANDIDATE_LIST_ITEM.format(**p)

    # pprint(candidates_str)
    # with open("index_template.html") as index:
    #     candidates_template=index.read().format(candidates_str)

    return template(page_str)  # template(candidates_template)
    # return template('<b>Hello {{name}}</b>!', name=name)


if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True, reloader=True)
    # jhgfjhfgj
