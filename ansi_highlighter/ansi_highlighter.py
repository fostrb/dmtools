import re
from collections import OrderedDict

# TODO: Regex isn't returning submatches.
# TODO: substring matching for bg highlights is terribly slow.
# TODO: make regex unaware of newlines - for text-wrapped input


class AnsiHighlighter(object):
    def __init__(self, highlight_dict, search_terms):
        self.fg_highlights = highlight_dict
        self.search_terms = search_terms

        self.fg_list = []

    def build_fg_regex(self):
        rstr = ''
        for key, val in self.fg_highlights.items():
            rstr += "(" + key + ")|"
            self.fg_list.append(val)
        rstr = rstr[:-1]
        return rstr

    def build_bg_regex(self):
        return ''
        rstr = ''
        for key in self.search_terms:
            rstr += "(" + key + ")|"
        #rstr = rstr[:-1]
        return rstr

    def highlight(self, text):
        bg_regex_str = self.build_bg_regex()
        full_regex_str = str(bg_regex_str) + str(self.build_fg_regex())
        bg_regex = re.compile(r'{}'.format(full_regex_str), re.I)

        i = 0
        h_output = ''

        for m in bg_regex.finditer(text):
            # print(m.group())
            hl_prefix = ''
            hl_suffix = ''
            #print(m.group())
            '''
            for match in m.groups():
                if match is not None:
                    # apply background
                    for search in self.search_terms:
                        if re.match(match, search, re.I):
                            hl_prefix += '\x1b[7m'
                            hl_suffix += '\x1b[27m'
                    # apply foreground
                    for fg_m, fg_v in self.fg_highlights.items():
                        if re.match(match, fg_m, re.I):
                            hl_prefix += '\x1b[38;5;' + self.fg_highlights[fg_m] + 'm'
                            hl_suffix += '\x1b[39m'
            '''

            hl_prefix += '\x1b[38;5;' + self.fg_list[m.lastindex-1] + 'm'
            hl_suffix += '\x1b[39m'

            h_output += "".join([text[i:m.start()], hl_prefix, text[m.start():m.end()], hl_suffix])
            i = m.end()

        if h_output != '':
            return "".join([h_output, text[i:]])
        else:
            return text


if __name__ == '__main__':
    fg_highlights = OrderedDict({
        'strength'      : '160',  # red
        'dexterity'     : '190',  # yellow
        'constitution'  : '100',  # brown-ish
        'intelligence'  : '201',  # purple
        'wisdom'        : '219',  # pink
        'charisma'      : '51',  # blue
    })

    text = "strength is a thing that should be highlighted. Wisdom too. constitution intelligence"
    search = ['str']
    hl = AnsiHighlighter(fg_highlights, search)
    out = hl.highlight(text)
    print(out)
