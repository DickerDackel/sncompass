import datetime

import pymongo

from pymongo import MongoClient
from bson.objectid import ObjectId

from sncompass import conf


connect, db_name = conf['mongodb']['MONGODB_URL'].rsplit('/', maxsplit=1)
client = MongoClient(connect)
db = client[db_name]


class Categories:
    def __init__(self):
        self.collection = db.categories

    def all(self):
        return [ c['category'] for c in list(self.collection.find({})) ]


class LocationConflict(BaseException):
    def __init__(self, message, name, location):
        super().__init__(self, message)
        self.name = name
        self.location = location


class Locations:
    def __init__(self):
        self.collection = db.locations

    @staticmethod
    def _near_query(x, y, z, name=None):
        query = {'$and': [
            {'x': {'$gte': x - 10, '$lte': x + 10}},
            {'y': {'$gte': y - 10, '$lte': y + 10}},
            {'z': {'$gte': z - 10, '$lte': z + 10}},
        ]}

        if name:
            query = {'$or': [
                query,
                {'name': name }
            ]}

        return query

    def by_id(self, id):
        return self.collection.find_one({'_id': ObjectId(id)})

    def find(self, x, y, z, name=None):
        return self.collection.find(Locations._near_query(x, y, z, name)).sort('name')

    def has(self, x, y, z, name=None):
        return self.collection.count_documents(Locations._near_query(x, y, z, name))

    def all(self):
        locations = {}
        for loc in self.collection.find({}).sort([
                ('category', pymongo.ASCENDING),
                ('name', pymongo.ASCENDING) ]):
            cat = loc['category']
            if cat not in locations:
                locations[cat] = [loc]
            else:
                locations[cat].append(loc)

        return locations

    def delete(self, id):
        # Don't delete the origin
        deleted = self.collection.delete_one(
            {'$and': [
                {'immutable': False},
                {'_id': ObjectId(id)}
            ]}
        )

        return deleted

    def add(self, x, y, z, name, submitter):
        match = list(self.find(x, y, z, name))
        if len(match):
            raise LocationConflict('Location conflict', match[0]['name'], (match[0]['x'], match[0]['y'], match[0]['z']))

        self.collection.insert_one(
            {
                'category': 'User submitted',
                'x': x, 'y': y, 'z': z,
                'name': name,
                'submitter': submitter,
                'created': datetime.datetime.isoformat(datetime.datetime.now()),
            }
        )
