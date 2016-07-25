__author__ = 'mstacy'
import ast
import math
import collections
from bson.objectid import ObjectId
from ordereddict import OrderedDict
from rest_framework.templatetags.rest_framework import replace_query_param

def MongoDistinct(field,DB_MongoClient, database, collection, query=None):
    db = DB_MongoClient
    if query:
        query = ast.literal_eval(query)
        #q = [(k, v) for k, v in query['spec'].items()]
        #query['spec'] = dict(q)
        return db[database][collection].find(**query).distinct(field)
    return db[database][collection].distinct(field)


def MongoDataPagination(DB_MongoClient, database, collection, query=None, page=1, nPerPage=None, uri=''):
    db = DB_MongoClient
    if query:
        query = ast.literal_eval(query)
        q = [(k, v) for k, v in query['filter'].items()]
        query['filter'] = dict(q)
        #print query
        count = db[database][collection].find(**query).count()
        #print count
        if nPerPage == 0:
            page=1
            offset=0
            max_page=1
        else:
            max_page = math.ceil(float(count) / nPerPage)
            # Page min is 1
            if page < 1:
                page = 1
            #Change page to last page with data
            if page * nPerPage > count:
                page = int(max_page)
            #Cover count =0
            if page < 1:
                page = 1
            offset = (page - 1) * nPerPage
        data = [row for row in db[database][collection].find(**query).skip(offset).limit(nPerPage)]
        #replace_query_param(uri, 'page', page)
    else:
        count = db[database][collection].find().count()
        if nPerPage == 0:
            page=1
            offset=0
            max_page=1
        else:
            max_page = math.ceil(float(count) / nPerPage)
            print max_page
            # Page min is 1
            if page < 1:
                page = 1
            #Change page to last page with data
            if page * nPerPage > count:
                page = int(max_page)
            #Cover count =0
            if page < 1:
                page = 1
            offset = (page - 1) * nPerPage
        data = [row for row in db[database][collection].find().skip(offset).limit(nPerPage)]
    if page < max_page:
        next = replace_query_param(uri, 'page', page + 1)
    else:
        next = None
    if page > 1:
        previous = replace_query_param(uri, 'page', page - 1)
    else:
        previous = None
    result = {'count': count, 'meta': {'page': page, 'page_size': nPerPage, 'pages': int(max_page)}, 'next': next,
              'previous': previous, 'results': data}

    try:
        od = collections.OrderedDict(sorted(result.items()))
    except:
        # older python versions < 2.7
        od = OrderedDict(sorted(result.items()))
    return od

def MongoDataGet(DB_MongoClient, database, collection,id):
    db = DB_MongoClient
    return db[database][collection].find_one({'_id':ObjectId(id)})
