from pymongo import MongoClient
import argparse
from collections import OrderedDict
import re

# TODO: levels are stored in db as integers. Makes regex matches a little less than fun. Custom search probably better.
# TODO: flag for query type (and/or/etc...)


# this isn't what we want to use for classes. or pretty much anything but levels.
def build_or_regex(opt_list):
    regex_str = ''
    for opt in opt_list:
        regex_str += '(' + opt + ')|'
    regex_str = regex_str[:-1]
    regex = re.compile('{}'.format(regex_str), re.I)
    return regex


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, nargs='*', action='store', dest='classes')
    parser.add_argument('-l', type=str, nargs='*', action='store', dest='levels')

    opts = []
    args = parser.parse_args()

    if args.classes:
        cdict = {}
        cdict['cclasses'] = build_or_regex(args.classes)
        opts.append(cdict)

    if args.levels:
        print(args.levels)
        ldict = {}
        ldict['levels'] = build_or_regex(args.levels)
        print(ldict)
        opts.append(ldict)

    client = MongoClient('localhost', 27017)
    # client = MongoClient()
    db = client.spelldb
    spells = db.spells

    # class_regex = re.compile('cleric', re.I)
    spells_returned = 0
    # for spell in spells.find({"$and": [{'cclasses': class_regex}, {'level': 0}]}):
    for spell in spells.find({"$and": opts}):
        spells_returned += 1
        print(spell['name'])
    print(spells_returned)
