from pymongo import MongoClient
import re

# TODO: switch for query type (and/or/etc...)


def build_search(opts):
    pass


def intersection_search(search_objects):
    stype = "$and"


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    #client = MongoClient()
    db = client.spelldb
    spells = db.spells

    class_regex = re.compile('cleric', re.I)

    spells_returned = 0
    for spell in spells.find({"$and": [{'cclasses': class_regex}, {'level': 0}]}):
        spells_returned += 1
        print(spell['name'])
    print(spells_returned)
