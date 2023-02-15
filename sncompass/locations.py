import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId

class LocationConflict(BaseException):
    def __init__(self, message, name, location):
        super().__init__(self, message)
        self.name = name
        self.location = location

class Locations:
    def __init__(self, url):
        connect, db = url.rsplit('/', maxsplit=1)
        client = MongoClient(connect)

        self.db = client[db]

    @staticmethod
    def _gen_near_query(x, y, z):
        return {
            '$and': [
                {'x': {'$gte': x-10, '$lte': x+10}},
                {'y': {'$gte': y-10, '$lte': y+10}},
                {'z': {'$gte': z-10, '$lte': z+10}},
            ]
    }

    @staticmethod
    def _gen_exact_query(x, y, z):
        return {
            '$and': [
                {'x': {'$eq': x}},
                {'y': {'$eq': y}},
                {'z': {'$eq': z}},
            ]
    }

    def by_id(self, id):
        return self.db.locations.find_one({'_id': id})

    def find(self, x, y, z):
        return self.db.locations.find(Locations._gen_near_query(x, y, z)).sort('name')

    def has(self, x, y, z):
        return self.db.locations.count_documents(Locations._gen_near_query(x, y, z))

    def all(self):
        return self.db.locations.find({}).sort('name')

    def delete(self, id):
        # Don't delete the origin
        res = self.db.locations.delete_one(
            {'$and': [
                {'immutable': false},
                {'x': {'$ne': 0}},
                {'y': {'$ne': 0}},
                {'z': {'$ne': 0}},
                {'_id': ObjectId(id)}
            ]}
        )

    def add(self, name, submitter, x, y, z):
        rec = {
            'name': name,
            'submitter': submitter,
            'x': x, 'y': y, 'z': z,
            'created': datetime.datetime.isoformat(datetime.datetime.now()),
        }

        match = list(self.find(x, y, z))
        if len(match):
            raise LocationConflict('Location conflict', match[0]['name'], (match[0]['x'], match[0]['y'], match[0]['z']))

        self.db.locations.insert_one(rec)
