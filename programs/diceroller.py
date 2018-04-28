from programs.program import DMProgram
from arpeggio import Optional, ZeroOrMore, OneOrMore, ParserPython, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _
import random

# calculator, supports dice notation
#   "3d4" will roll 3d4 and return the sum
#   "d8" will roll 1d8 and return result
#
#   "3d4!" rolls 3d4, rolling again on each 'crit', returning total sum
#   "3d4K" keeps highest roll
#   "3d4k" keeps lowest roll
#   "3d4X" dumps highest roll
#   "3d4x" dumps lowest roll
#   "3d4R" rerolls for each crit
#   "3d4r" rerolls each 1
#   Each die roll evaluates as a number, and can be operated upon.
#   There are safeguards for infinite looping on D1s within !, R, and r


class Roll(DMProgram):
    def __init__(self):
        super(Roll, self).__init__()
        self.name = 'roll'
        self.aliases = ['r']

    def run(self, line):
        parser = ParserPython(roll)
        parse_tree = parser.parse(line)
        result = visit_parse_tree(parse_tree, DiceCalcuator(debug=False))
        return result


def die():
    return Optional(number), "d", number, Optional(["!", 'K', 'k', 'X', 'x', 'R', 'r'])


def number():
    return _(r'\d*\.\d*|\d+')


def factor():
    return Optional(["+", "-"]), [die, number, ("(", expression, ")")]


def term():
    return factor, ZeroOrMore(["*", "/"], factor)


def expression():
    return term, ZeroOrMore(["+", "-"], term)


def roll():
    return OneOrMore(expression)


class DiceCalcuator(PTNodeVisitor):
    def visit_number(self, node, children):
        if self.debug:
            print("Converting {}.".format(node.value))
        return node.value

    def visit_factor(self, node, children):
        if self.debug:
            print("Factor {}".format(children))
        if len(children) == 1:
            return children[0]
        sign = -1 if children[0] == '-' else 1
        return sign * children[-1]

    def visit_term(self, node, children):
        if self.debug:
            print("Term {}".format(children))
        term = children[0]
        for i in range(2, len(children), 2):
            if children[i-1] == "*":
                term *= children[i]
            else:
                term /= children[i]
        if self.debug:
            print("Term = {}".format(term))
        return term

    def visit_die(self, node, children):
        rval = 0
        numdice = 1
        modifier = None
        dicepool = []
        die = int(children[0])

        if len(children) >= 2:
            try:
                numdice = int(children[0])
                die = int(children[1])
                if len(children) >= 3:
                    modifier = children[2]
            except:
                numdice = 1
                modifier = children[1]

        if modifier is None:
            for each in range(numdice):
                thisroll = random.randint(1, die)
                dicepool.append(thisroll)
                rval += thisroll
        elif modifier == "!":
            if die == 1:
                return 0
            # Explode! (each die rolls again if max)
            for each in range(numdice):
                thisroll = die
                while thisroll == die:
                    thisroll = random.randint(1, die)
                    rval += thisroll
                    if thisroll == die:
                        dicepool.append(str(thisroll) + '!')
                    else:
                        dicepool.append(thisroll)
        elif modifier == "K":
            # keep highest one
            for each in range(numdice):
                thisroll = random.randint(1, die)
                dicepool.append(thisroll)
            dicepool = sorted(dicepool)
            highest = dicepool[-1]
            rval = highest
        elif modifier == "k":
            #keep lowest one
            for each in range(numdice):
                thisroll = random.randint(1, die)
                dicepool.append(thisroll)
            dicepool = sorted(dicepool)
            lowest = dicepool[0]
            rval = lowest
        elif modifier == "X":
            # Drop highest
            for each in range(numdice):
                thisroll = random.randint(1, die)
                dicepool.append(thisroll)
            dicepool = sorted(dicepool)
            dicepool.pop(-1)
            rval = sum(dicepool)
        elif modifier == "x":
            # Drop lowest
            for each in range(numdice):
                thisroll = random.randint(1, die)
                dicepool.append(thisroll)
            dicepool = sorted(dicepool)
            dicepool.pop(0)
            rval = sum(dicepool)
        elif modifier == "R":
            if die == 1:
                return 0
            # Reroll on Max
            for each in range(numdice):
                while True:
                    thisroll = random.randint(1, die)
                    if thisroll != die:
                        break
                dicepool.append(thisroll)
            dicepool = sorted(dicepool)
            rval = sum(dicepool)
        elif modifier == "r":
            if die == 1:
                return 0
            # Reroll ones
            for each in range(numdice):
                while True:
                    thisroll = random.randint(1, die)
                    if thisroll != 1:
                        break
                dicepool.append(thisroll)
            dicepool = sorted(dicepool)
            rval = sum(dicepool)

        print(dicepool)
        return rval

    def visit_expression(self, node, children):
        if self.debug:
            print("Expression {}".format(children))
        expr = children[0]
        for i in range(2, len(children), 2):
            if i and children[i - 1] == "-":
                expr -= children[i]
            else:
                expr += children[i]
        if self.debug:
            print("Expression = {}".format(expr))
        return expr