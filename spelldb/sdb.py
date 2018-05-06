from pymongo import MongoClient
from mongoengine import *
import json

# TODO: keep plodding through the dumb data.

# client = MongoClient()
# db = client.mongoengine_test



class Spell(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    classes = ListField(required=True)
    level = IntField(required=True)
    higher_level = StringField(required=True)
    range = StringField(required=True)

db = connect('spelldb', host='localhost', port=27017)

'''
with open('better_spelldump.json') as fdata:
    spells = json.load(fdata)



print(db)

for spell in spells:
    print(spell['range'])
    print(spell['level'])
    # optionals here
    if 'higher_level' in spell.keys():
        higher_level = spell['higher_level']
    else:
        higher_level = ''
    if 'range' in spell.keys():
        sprange = spell['range']
    else:
        sprange = ''

    s = Spell(
        name=spell['name'],
        description=spell['description'],
        classes=spell['classes'],
        level=spell['level'],
        higher_level=higher_level,
        range=sprange
    )
    s.save()
'''

for s in Spell.objects:
    print(s.name)
    print(s.classes)

print(len(Spell.objects))
