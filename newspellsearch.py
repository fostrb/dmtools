import argparse
import json
import textwrap
import re
from random import randint
from collections import OrderedDict

from ansi_highlighter.ansi_highlighter import AnsiHighlighter

# TODO: database would be easier and cleaner than json

# TODO: add filters for archetypes, domains, etc...
# TODO: implement union/intersect/etc within class search/filter
# TODO: print formatting update

# TODO: sort by field (put this shit in a database)

# TODO: add a switch for highlighted printing

'''
notes:
- This is insanely slow on crappy machines - it's the highlighter.
    The highlighter attempts to match for each group in each match
        from the master regex's iteritems(). Meaning, most of them
        will be Null matches, and therefore useless.
        
    The good solution: just fix the existing code.
    The solution that sounds cool: Totally separate the text 
        generator and the highlight display.
'''

# output:
# <name>
# <level> <school>
#


# to be used for highlighting searches
SEARCH_TERMS = []

# print flag: "n: just names, s: short"
PRINT_FLAG = False


HIGHLIGHTS = OrderedDict({
    # abilities -------------------------------------
    'strength'      : '196',  # red
    'dexterity'     : '190',  # yellow
    'constitution'  : '100',  # brown-ish
    'intelligence'  : '201',  # purple
    'wisdom'        : '219',  # pink
    'charisma'      : '51',  # blue

    # keywords
    'saving throw'  : '203',  # salmon-ish

    # schools of magic
    # abjuration
    # conjuration
    # divination
    # enchantment
    # evocation
    # illusion
    # necromancy
    # transmutation

    # concentration
    'concentration' : '39',  # sorta blue
    # ritual


    # dice regex
    '\d+d\d+'          : '130',  # blue

    # damage types (regex [optional 'damage'])
    'psychic damage': '207',  # purple
    'bludgeoning damage': '130',  # brown
    'slashing damage': '130',  # orange
    'piercing damage': '226',  # yellow
    'fire damage': '160',  # red
    'acid damage': '120',  # green
    'cold damage': '123',  # light blue
    'force damage': '95',  # weird brown
    'lightning damage': '226',  # yellow
    'thunder damage': '33',  # blue
    'necrotic damage': '66',  # grey green
    'poison damage': '82',  # green
    'radiant damage': '15'  # white

    # range regex: "touch"|number"feet"|other shit

    # action regex: bonus, free, etc
    # 1 action
    # bonus action
    # reaction

    # Save DC
    # Spell attack (melee, ranged, etc)
})


def filter_random(random, spells):
    try:
        r = int(random)
        rlist = []

        if r <= len(spells):
            for i in range(r):
                index = 0
                while spells[index] not in rlist:
                    index = randint(0, len(spells)-1)
                    rlist.append(spells[index])
            return rlist

        else:
            print("Length of previously filtered spells is " + str(len(spells)) + "\n"
                "random " + str(r) + " failed.")
            #return spells
            exit(1)
    except AttributeError as e:
        print(e)
        exit(1)


def filter_description(general, spells):
    filtered_spells = []
    filter_list = general.split(',')
    for spell in spells:
        if spell not in filtered_spells:
            for search in filter_list:
                if search in (spell['description']):
                    filtered_spells.append(spell)
    return filtered_spells


def filter_classes(classes, spells):
    filter_list = classes.split(',')
    filtered_spells = []
    for spell in spells:
        get = True
        if spell not in filtered_spells:
            for search in filter_list:
                regex = re.compile(r'{}'.format(search), re.I)
                subget = False
                for c in spell['classes']:
                    if regex.match(c):
                        subget = True
                if not subget:
                    get = False
            if get:
                filtered_spells.append(spell)
    return filtered_spells


def filter_gen(filters, spells):
    filtered_spells = []
    for spell in spells:
        if spell not in filtered_spells:
            get = True
            for filter in filters:
                if filter not in SEARCH_TERMS:
                    SEARCH_TERMS.append(filter)
                if filter not in str(spell):
                    get = False
            if get:
                filtered_spells.append(spell)
    return filtered_spells


def filter_name(names, spells):
    filter_list = names.split(',')
    filtered_spells = []

    for search in filter_list:
        regex = re.compile(r'{}'.format(search), re.I)
        for spell in spells:
            if regex.match(spell['name']):
                if spell not in filtered_spells:
                    filtered_spells.append(spell)
    return filtered_spells


def filter_levels(levels, spells):
    # generate a list of levels that matches the input level string(s)
    filtered_spells = []
    filter_list = levels.split(',')

    for search in filter_list:
        regex = re.compile(r'{}'.format(search), re.I)
        for spell in spells:
            if regex.match(str(spell['level'])):
                if spell not in filtered_spells:
                    filtered_spells.append(spell)
    return filtered_spells


def print_spell(spell):
    name = spell['name']

    components = spell['components']

    is_verbal = False
    is_somatic = False
    is_material = False

    if "V" in components:
        is_verbal = True
    if "S" in components:
        is_somatic = True
    if "M" in components:
        is_material = True

    raw_components = ",".join(components)

    description = spell['description']
    casting_time = spell['casting_time']
    classes = spell['classes']  # list of strings

    duration = spell['duration']
    level = spell['level']
    range = spell['range']
    ritual = spell['ritual']  # bool
    school = spell['school']
    if PRINT_FLAG:
        output = ''
        #just names
        if PRINT_FLAG == 'n':
            output = name

        #short
        elif PRINT_FLAG == 's':
            output += name + '\n'
            output += "Casting Time: " + casting_time + '\n'
    else:
        output = name + '\n'
        output += '-' * 80 + '\n'
        output += textwrap.fill(raw_components, 80) + '\n'
        output += textwrap.fill("Casting Time: " + casting_time, 80) + '\n'
        output += textwrap.fill(description, 80) + '\n'
        output += '-' * 80

    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # for now, pass a comma separated list and parse on your own
    parser.add_argument("-i", '--infile', type=str, action='store', dest='infile',
                        help='Import a json file of spells to work with instead of the entire list.')
    parser.add_argument("-e", '--export', type=str, action='store', dest='export',
                        help='Json dump query to a file.')
    parser.add_argument("-c", "--class", type=str, action='store', dest='classes',
                        help="Search class names.")
    parser.add_argument("-n", "--names", type=str, action='store', dest='names',
                        help="Search spell names")
    parser.add_argument("-l", "--levels", type=str, action='store', dest='levels',
                        help="Filter by spell level.")
    parser.add_argument("-p", "--print", type=str, action='store', dest='print',
                        help="Print formatting. 's'=short, 'n'=just names.")
    parser.add_argument("-d", "--description", type=str, action='store', dest='description',
                        help='Filter by description.')
    parser.add_argument("-r", "--random", type=str, action='store', dest='random',
                        help="Choose X spells from filtered list. This filter will run last.")
    parser.add_argument("gen", default=[], nargs='*', action='store',
                        help="Filter the spell's raw Json.")
    args = parser.parse_args()
    SPELLS = []
    if not args.infile:
        with open('data/better_spelldump.json') as json_data:
            SPELLS = json.load(json_data)
    else:
        try:
            with open(args.infile) as json_data:
                SPELLS = json.load(json_data)
        except:
            print("issue with your file")
            exit(1)
    if args.print:
        if args.print in ['n', 's']:
            PRINT_FLAG = args.print
    spells = SPELLS
    if args.classes:
        spells = filter_classes(args.classes, spells)
    if args.names:
        spells = filter_name(args.names, spells)
    if args.levels:
        spells = filter_levels(args.levels, spells)
    if args.description:
        spells = filter_description(args.general, spells)
    if args.gen:
        spells = filter_gen(args.gen, spells)

    if args.random:
        spells = filter_random(args.random, spells)
    outputstr = ''

    highlighter = AnsiHighlighter(HIGHLIGHTS, search_terms=SEARCH_TERMS)
    for spell in spells:
        outputstr += print_spell(spell) + '\n'
    print(highlighter.highlight(outputstr))
    print(str(len(spells)) + " spells matched criteria.")
    if args.export:
        try:
            with open(args.export, 'w') as exportFile:
                json.dump(spells, fp=exportFile)
        except:
            print("issue exporting")

# search criteria:

# spell is a ritual
# class matches "string"
# is_verbal/somatic/material
# casting time: action, bonus, reaction, minute(s), hour(s)
# duration
# range
# school matches string
# does damage | average damage (requires parsing dice)
# is AOE
