import argparse
import json
import textwrap
import re
from collections import OrderedDict

# TODO: Improper highlighter behavior when user searches overlap builtin regexes.
# A solution might be to not hard-code the entire escape values, and break them into
#   text color for hard-coded matches, and reverse behavior\bg highlight for searches.


# to be used for highlighting searches
SEARCH_TERMS = []
highlights = []

# print flag: "n: just names, s: short"
PRINT_FLAG = False


HIGHLIGHTS = OrderedDict({
    # abilities -------------------------------------
    'strength'      : '\033[38;5;196m',  # red
    'dexterity'     : '\033[38;5;190m',  # yellow
    'constitution'  : '\033[38;5;100m',  # brown-ish
    'intelligence'  : '\033[38;5;201m',  # purple
    'wisdom'        : '\033[38;5;219m',  # pink
    'charisma'      : '\033[38;5;51m',  # blue

    # keywords
    'saving throw'  : '\033[38;5;203m',  # salmon-ish

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
    'concentration' : '\033[38;5;39m',  # sorta blue
    # ritual


    # dice regex
    '\d+d\d+'          : '\033[38;5;130m',  # blue

    # damage types (regex [optional 'damage'])
    'psychic damage': '\033[38;5;207m',  # purple
    'bludgeoning damage': '\033[38;5;130m',  # brown
    'slashing damage': '\033[38;5;130m',  # orange
    'piercing damage': '\033[38;5;226m',  # yellow
    'fire damage': '\033[38;5;160m',  # red
    'acid damage': '\033[38;5;120m',  # green
    'cold damage': '\033[38;5;123m',  # light blue
    'force damage': '\033[38;5;95m',  # weird brown
    'lightning damage': '\033[38;5;226m',  # yellow
    'thunder damage': '\033[38;5;33m',  # blue
    'necrotic damage': '\033[38;5;66m',  # grey green
    'poison damage': '\033[38;5;82m',  # green
    'radiant damage': '\033[38;5;15m'  # white


    # range regex: "touch"|number"feet"|other shit

    # action regex: bonus, free, etc
    # 1 action
    # bonus action
    # reaction

    # Save DC
    # Spell attack (melee, ranged, etc)
})


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
    # generate a list of levels that matches the input level string
    filtered_spells = []
    filter_list = levels.split(',')

    for search in filter_list:
        if search == '0':
            regex = re.compile(r'{}'.format('cantrip'), re.I)
        else:
            regex = re.compile(r'{}'.format(search), re.I)
        for spell in spells:
            if regex.match(spell['level']):
                if spell not in filtered_spells:
                    filtered_spells.append(spell)
    return filtered_spells


def print_spell(spell):
    name = spell['name']

    components = spell['components']
    is_verbal = components['verbal']  # bool
    is_somatic = components['somatic']  # bool
    is_material = components['material']  # bool
    raw_components = components['raw']  # str("v,s,m")

    description = spell['description']
    casting_time = spell['casting_time']
    classes = spell['classes']  # list of strings

    duration = spell['duration']
    level = spell['level']
    range = spell['range']
    ritual = spell['ritual']  # bool
    school = spell['school']
    tags = spell['tags']  # list of strings
    type = spell['type']  # x lvl school (ritual)
    if PRINT_FLAG:
        output = ''
        #just names
        if PRINT_FLAG == 'n':
            #print("here", name)
            output = name


        #short
        elif PRINT_FLAG == 's':
            output += name + '\n'
            output += type + '\n'
            output += "Casting Time: " + casting_time + '\n'
    else:
        output = name + '\n'
        output += '-' * 80 + '\n'
        output += textwrap.fill(type, 80) + '\n'
        output += textwrap.fill(raw_components, 80) + '\n'
        output += textwrap.fill("Casting Time: " + casting_time, 80) + '\n'
        output += textwrap.fill(description, 80) + '\n'
        output += '-' * 80

    return output


def build_highlighter_regex():
    rstr = ''
    for key in SEARCH_TERMS:
        HIGHLIGHTS[key] = '\033[1;31;40m'
    for key, val in HIGHLIGHTS.items():
        rstr += "(" + key + ")|"
        highlights.append(val)
    rstr = rstr[:-1]
    return rstr


def highlighter(text):
    regexstr = build_highlighter_regex()
    regex = re.compile(r'{}'.format(regexstr), re.I)
    i = 0
    h_output = ''
    for m in regex.finditer(text):
        h_output += "".join([text[i:m.start()], highlights[m.lastindex-1], text[m.start():m.end()], '\033[0m'])
        i = m.end()
    try:
        if h_output != '':
            print(h_output)
        else:
            print(text)
    except:
        print(text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # for now, pass a comma separated list and parse on your own
    parser.add_argument("-i", '--import', type=str, action='store', dest='import')
    parser.add_argument("-c", "--class", type=str, action='store', dest='classes')
    parser.add_argument("-n", "--names", type=str, action='store', dest='names')
    parser.add_argument("-l", "--levels", type=str, action='store', dest='levels')
    parser.add_argument("-p", "--print", type=str, action='store', dest='print')
    parser.add_argument("-d", "--description", type=str, action='store', dest='description')
    parser.add_argument("gen", default=[], nargs='*', action='store')
    args = parser.parse_args()

    with open('/home/fostrb/PycharmProjects/dmshell/data/newspells.json') as json_data:
        SPELLS = json.load(json_data)
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

    outputstr = ''
    for spell in spells:
        outputstr += print_spell(spell) + '\n'
    highlighter(outputstr)
    print(str(len(spells)) + " spells matched criteria.")

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

