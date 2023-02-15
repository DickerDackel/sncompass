#!/bin/env python3

import json

from pprint import pprint
from pymongo import MongoClient

client = MongoClient('mongodb://mongodb')
db = client.subnautica

print('########################################################################')
print('Collections:')
print('########################################################################')
collections = list(db.list_collection_names())
for c in collections:
    print(' ' * 4, c)

print()
for c in collections:
    print('========================================================================')
    print(c)
    print('========================================================================')

    docs = list(db[c].find({}))
    for d in docs:
        pprint(d)
        # print(json.dumps(d, indent=4, sort_keys=True))
