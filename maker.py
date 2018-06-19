import re
import math


def create_TOC(file, name):
    link = True
    lines = [line.rstrip('\n') for line in open(file)]  # get lines

    last_line = ""
    last_line_valid = False

    in_code_block = False

    # content selection
    toc_texts = []
    for line in lines:
        current_line_valid = True

        if line.lower() == name.lower():  # ignore TOC (case insensitive)
            current_line_valid = False

        # multiline code check
        if re.match("^\s*(`){3}", line) != None:
            current_line_valid = False
            in_code_block = not in_code_block

        # headers check
        if not in_code_block:

            # diese header check
            if re.match("^( ){0,3}(#{1,6})( )+", line) != None:
                toc_texts += [line]
                current_line_valid = False

            # underline header check
            elif last_line_valid and re.match("^( ){0,3}(-{3,})$", line) != None:
                toc_texts += ["|L1|"+last_line]  # add mark
                current_line_valid = False
            elif last_line_valid and re.match("^( ){0,3}(={3,})$", line) != None:
                toc_texts += ["|L0|"+last_line]  # add mark
                current_line_valid = False

        # check for line break (***, ---)
        if re.match("^[\s\-*]{3,}$", line):
            current_line_valid = False

        # you actualy can make a title underlined with content '===' or '---'
        # those will therefore be allowed

        # check for validity - last_line_valid update
        if not current_line_valid:
            last_line_valid = False
            last_line = "__INVALID__ : " + line
        else:
            # suppose it is valid at this point
            last_line_valid = True
            last_line = line

    # TOC creation
    toc_text = name + "\n" + len(name) * "=" + "\n\n"

    for text in toc_texts:
        level = math.nan

        # remove mark and set level
        if re.match("^\|L0\|( ){0,3}", text) != None:
            text = re.sub("^\|L0\|( ){0,3}", "", text)
            level = 0
        elif re.match("^\|L1\|( ){0,3}", text) != None:
            text = re.sub("^\|L1\|( ){0,3}", "", text)
            level = 1  # trim

        # remove diese header and set level
        if re.match("^( ){0,3}(#{1})( )+", text) != None:
            text = re.sub("^( ){0,3}(#{1})( )+", "", text)
            level = 0
        elif re.match("^( ){0,3}(#{2})( )+", text) != None:
            text = re.sub("^( ){0,3}(#{2})( )+", "", text)
            level = 1
        elif re.match("^( ){0,3}(#{3})( )+", text) != None:
            text = re.sub("^( ){0,3}(#{3})( )+", "", text)
            level = 2
        elif re.match("^( ){0,3}(#{4})( )+", text) != None:
            text = re.sub("^( ){0,3}(#{4})( )+", "", text)
            level = 3
        elif re.match("^( ){0,3}(#{5})( )+", text) != None:
            text = re.sub("^( ){0,3}(#{5})( )+", "", text)
            level = 4
        elif re.match("^( ){0,3}(#{6})( )+", text) != None:
            text = re.sub("^( ){0,3}(#{6})( )+", "", text)
            level = 5

        # create toc element (with url or not)
        if link:
            url = text.lower()
            url = re.sub('[\'\(\)/`=-]', '', url)  # remove ' ( ) / ` = -
            url = re.sub(' ', '-', url)  # replace spaces by -
            toc_text += 4 * level * " " + "* [" + text + "](#" + url + ")\n"
        else:
            toc_text += 4 * level * " " + "* [" + text + "]\n"

    return toc_text + "\n***\n"


# making it work
if __name__ == "__main__":
    print(create_TOC("README.md", "Table of Content"))


""" md RULES
underline header:
    max 3 blank space before
    min 1 =/- (no max)

diese header:
    max 3 blank space before the first #
    min 1 and max 6 #

quote block:
    starting with > (may be nested undefinitely, max 4 spaces between each >)
    ! can contain header only if # if the first non space or # char
    not to include in a table of content...

code block:
    start with at least 4 spaces or at least 1 tab or "```" or "`"
    ! canNOT contain header

    max 3 spaces before ```

    -> no need to check inline code (`) (first)

    # and nothing else
    -> no need to prevent 4 space / 1 tab before there should be max 3 space before

invalid text for header:
    quoted
    list
    tabed code block
    header line (full header)
    line full of =/-
"""
