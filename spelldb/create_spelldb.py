# from pymongo import MongoClient
from mongoengine import *
import json

# TODO: keep plodding through the dumb data.

# client = MongoClient()
# db = client.mongoengine_test


class Spells(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    cclasses = ListField(required=True)
    level = IntField(required=True)
    higher_level = StringField(required=False)
    range = StringField(required=True)
    components = ListField(required=True)
    casting_time = StringField(required=True)
    school = StringField(required=True)
    duration = StringField(required=True)
    ritual = BooleanField(required=True)
    source = StringField(required=True)
    materials = StringField(required=False)
    concentration = BooleanField(required=True)

    archetypes = DictField(required=False)
    domains = ListField(required=False)
    patrons = ListField(required=False)
    oaths = ListField(required=False)
    circles = ListField(required=False)
    subclass = ListField(required=False)


db = connect('spelldb', host='localhost', port=27017)

with open('better_spelldump.json') as fdata:
    spells = json.load(fdata)

print(db)

for spell in spells:
    # optionals here
    if 'higher_level' in spell.keys():
        higher_level = spell['higher_level']
    else:
        higher_level = None

    if 'range' in spell.keys():
        sprange = spell['range']
    else:
        sprange = None

    if 'material' in spell.keys():
        spell_materials = spell['material']
    else:
        spell_materials = ''

    if 'domains' in spell.keys():
        spell_domains = spell['domains']
    else:
        spell_domains = []

    if 'patrons' in spell.keys():
        spell_patrons = spell['patrons']
    else:
        spell_patrons = []

    if 'oaths' in spell.keys():
        spell_oaths = spell['oaths']
    else:
        spell_oaths = []

    if 'circles' in spell.keys():
        spell_circles = spell['circles']
    else:
        spell_circles = []

    if 'subclass' in spell.keys():
        print("here")
        spell_subclass = spell['subclass']
        print(spell_subclass)
    else:
        spell_subclass = []

    if 'archetypes' in spell.keys():
        spell_archetypes = spell['archetypes']
    else:
        spell_archetypes = {}

    s = Spells(
        name=spell['name'],
        description=spell['description'],
        cclasses=spell['cclasses'],
        level=spell['level'],
        higher_level=higher_level,
        range=sprange,
        components=spell['components'],
        casting_time=spell['casting_time'],
        school=spell['school'],
        duration=spell['duration'],
        ritual=spell['ritual'],
        source=spell['source'],
        materials=spell_materials,
        concentration=spell['concentration'],

        archetypes=spell_archetypes,
        domains=spell_domains,
        patrons=spell_patrons,
        oaths=spell_oaths,
        circles=spell_circles,
        subclass=spell_subclass
    )
    s.save()


for s in Spells.objects:
    print(s.name)
    #print(s.classes)
    print(s.archetypes)

print(len(Spells.objects))
