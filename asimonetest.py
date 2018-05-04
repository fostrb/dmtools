import json
import re

# TODO: add limited html tag interpretation to cleanhtml


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


with open("data/asimonespells.json") as filedata:
    spells = json.load(filedata)

new_spell_data = []

for spell in spells:
    newspell = {}
    for key, val in spell.items():
        if key == 'name':
            newspell['name'] = spell['name']

        elif key == 'desc':
            # STRIP DESCRIPTION OF <p> </p> TAGS
            dstr = cleanhtml(val)
            newspell['description'] = dstr

        elif key == "level":
            lvlstr = spell['level']
            lvlchar = lvlstr[0]
            lvl = 0
            if lvlchar in ['c', 'C']:
                lvl = 0
            else:
                lvl = int(lvlchar)

            newspell['level'] = lvl

        elif key == 'higher_level':
            # STRIP DESCRIPTION OF <p> </p> TAGS
            hlstr = cleanhtml(val)
            newspell['higher_level'] = hlstr

        elif key == 'range':
            newspell['range'] = val

        elif key == 'components':
            comps = val.replace(' ', '')
            comps = comps.split(',')
            newspell['components'] = comps

        elif key == 'material':
            newspell['material'] = val

        elif key == 'page':
            newspell['source'] = val

        elif key == 'ritual':
            if val == 'yes':
                v = True
            elif val == 'no':
                v = False
            else:
                print("ERROR")
            newspell['ritual'] = v

        elif key == 'duration':
            newspell['duration'] = val

        elif key == 'concentration':
            if val == 'yes':
                v = True
            elif val == 'no':
                v = False
            else:
                print("ERROR")
            newspell['concentration'] = v

        elif key == 'casting_time':
            newspell['casting_time'] = val

        elif key == 'school':
            newspell['school'] = val

        elif key == 'class':
            classes = val.replace(' ', '').split(',')
            #print(classes)
            newspell['class'] = classes

        elif key == 'archetype':
            # This will need heavy cleanup.
            #print(val)
            pass

        elif key == 'domains':
            doms = val.replace(' ', '').split(",")
            newspell['domains'] = doms

        elif key == 'patrons':
            patrs = val.replace(' ', '').split(",")
            newspell['patrons'] = patrs

        elif key == 'oaths':
            oaths = val.replace(' ', '').split(",")
            newspell['oaths'] = oaths

        elif key == 'circles':
            circles = val.replace(' ', '').split(",")
            newspell['circles'] = circles

        elif key == 'subclass':
            #subclass = val.replace(' ', '').split(",")
            newspell['subclass'] = val

        else:
            print(key)
            exit(1)
    new_spell_data.append(newspell)

print(len(spells))

with open('better_spelldump.json', 'w') as nspelldoc:
    json.dump(new_spell_data, nspelldoc)

with open('better_spelldump.json') as spdoc:
    nspells = json.load(spdoc)

print(len(nspells))

