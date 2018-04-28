#!/usr/bin/python3
import argparse
import textwrap
import json
import re


MAX_TEXT_LENGTH = 600


LEVEL_STRING = {
    0: '{school} cantrip {ritual}',
    1: '1st level {school} {ritual}',
    2: '2nd level {school} {ritual}',
    3: '3rd level {school} {ritual}',
    4: '4th level {school} {ritual}',
    5: '5th level {school} {ritual}',
    6: '6th level {school} {ritual}',
    7: '7th level {school} {ritual}',
    8: '8th level {school} {ritual}',
    9: '9th level {school} {ritual}',
}

with open('../data/spells.json') as json_data:
    SPELLS = json.load(json_data)

num = 0
for name, spell in SPELLS.items():
    num+=1
    print(name)
    for key, val in spell.items():
        print(key, val)
print(num)
exit()


def print_spell(name, level, school, range, time, ritual, duration, components,
                material, text, source=None, source_page=None, **kwargs):
    header = LEVEL_STRING[level].format(school=school.lower(), ritual='ritual' if ritual else '').strip()

    if material is not None:
        text = "Requires " + material + ". " + text

    if source_page is not None:
        source += ' page %d' % source_page

    output = ''

    output += "Spell: " + name + ' \n'
    output += header + ' \n'
    output += "Range: " + range + ' \n'
    output += "Cast time: " + time + ' \n'
    output += "Duration: " + duration + ' \n'
    output += ",".join(components) + ' \n'
    output += "Source: " + source + ' \n'
    output += textwrap.fill(text, 80) + ' \n'
    highlighter(output)


HIGHLIGHTS = {
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
}
highlights = []


def build_regex():
    rstr = ''
    for key, val in HIGHLIGHTS.items():
        rstr += "(" + key + ")|"
        highlights.append(val)
    rstr=rstr[:-1]
    return rstr


def highlighter(text):
    regexstr = build_regex()
    regex = re.compile(r'{}'.format(regexstr), re.I)
    i = 0
    output = ''
    for m in regex.finditer(text):
        output += "".join([text[i:m.start()],
                        highlights[m.lastindex-1],
                        text[m.start():m.end()],
                        '\033[0m'])
        i = m.end()
    try:
        print("".join([output, text[m.end():]]))
        #print(output)
    except:
        print(text)
    # classes
    # saving throws
    #


def get_spells(classes=None, levels=None, schools=None, names=None):
    classes = {i.lower() for i in classes} if classes is not None else None
    schools = {i.lower() for i in schools} if schools is not None else None
    names = {i.lower() for i in names} if names is not None else None

    return [
        (name, spell) for name, spell in sorted(SPELLS.items(), key=lambda x: x[0]) if
        (classes is None or len(classes & {i.lower() for i in spell['classes']}) > 0) and
        (schools is None or spell['school'].lower() in schools) and
        (levels is None or spell['level'] in levels) and
        (names is None or name.lower() in names)
    ]


def parse_levels(levels):
    rv = None
    if levels is not None:
        rv = set()
        for level_spec in levels:
            tmp = level_spec.split('-')
            if len(tmp) == 1:
                rv.add(int(tmp[0]))
            elif len(tmp) == 2:
                rv |= set(range(int(tmp[0]), int(tmp[1]) + 1))
    return rv


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--class", type=str, action='append', dest='classes',
        help="only select spells for this class, can be used multiple times "
             "to select multiple classes."
    )
    parser.add_argument(
        "-l", "--level", type=str, action='append', dest='levels',
        help="only select spells of a certain level, can be used multiple "
             "times and can contain a range such as `1-3`."
    )
    parser.add_argument(
        "-s", "--school", type=str, action='append', dest='schools',
        help="only select spells of a school, can be used multiple times."
    )
    parser.add_argument(
        "-n", "--name", type=str, action='append', dest='names',
        help="select spells with one of several given names."
    )

    parser.add_argument(
        "-d", "--dsearch", type=str, action='append', dest='dsearch',
        help="search descriptions for cool shit"
    )
    args = parser.parse_args()

    for name, spell in get_spells(args.classes, parse_levels(args.levels), args.schools, args.names):
        print_spell(name, **spell)
