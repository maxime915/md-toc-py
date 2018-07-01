#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import re
import math
import sys


def create_TOC(file, name, link):
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
    # if arg 1 and 2 are given (i.e. file name & TOC name)
    if len(sys.argv) == 3:
        print(create_TOC(sys.argv[1], sys.argv[2], True))
    # if linker option is set
    elif len(sys.argv) == 4:
        if sys.argv[3].lower() in ['0', 'no', 'n', 'f', 'false']:
            print(create_TOC(sys.argv[1], sys.argv[2], False))
        else:
            print(create_TOC(sys.argv[1], sys.argv[2], True))
    else:
        print("""
    MarkDown Table Of Content Maker
Please specify at least two arguments : the path for the markdown file and a name for your Table of Content. You may specify a third argument if you would like not to link your Table of Content by using the values "0", "no", "n", "f" or "false". If there is already a first type header in the markdown file having the title equal to the Table of Content name given (case insensitive), it will be ignored.

NB : requires python 3 installed

Usage :

    (linked TOC)
        python maker.py README.md Table\\ of\\ Contents

    (not linked)
        python maker.py README.md Table\\ of\\ Contents 0
""")
