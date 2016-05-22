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