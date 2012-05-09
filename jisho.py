# !/usr/local/bin/python
# coding=utf-8

import urllib
import sys
import re

def main():
    if len(sys.argv) < 2:
        print ">>> ERROR: Please specify an input file"
        sys.exit()
    
    filename = ""
    outputFile = ""

    kanjiMode = False
    trimMode = False

    for index, arg in enumerate(sys.argv):
        if index != 0:
            if arg[0] == "-" and arg[1] == "k":
                kanjiMode = True
            elif arg[0] == "-" and arg[1] == "t":
                trimMode = True
            elif filename == "":
                filename = arg
            else:
                outputFile = arg
    
    f = None
    try:
        f = open(filename, 'r')
    except:
        print "Can't find the file called", filename
        sys.exit()
    
    """
    writeFile = None
    try:
        writeFile = open('', 'w')
    except:
        print "IO Error."
        sys.exit()
    """
    if kanjiMode:
        count = 0
        nextLine = f.readline()

        while nextLine != "":
            splitLine = nextLine.split("　")
            for item in splitLine:
                if item != '' and item != '\n':
                    print translate(fixLine(item))
                    count += 1
            nextLine = f.readline()
           
        print "Total Kanji:", count

    else:
        count = 0
        nextLine = f.readline()
     
        while nextLine != "":
            nextLine = fixLine(nextLine) 
            match = re.search("^(\d+)", nextLine)
            if match:
                print ""
                print "---", match.groups()[0], "---"
            else:
                print translate(nextLine)
                count += 1

            nextLine = f.readline()
        print "Total:", count
    print "Thank you, jisho.org! :)"
        

def translate(word):
    # Open the page
    urlopener = urllib.FancyURLopener()
    #print "Looking up:", word, "."
    opened = urlopener.open("http://jisho.org/words?jap="+word+"&eng=&dict=edict")
    html = opened.read()

    # These are some nasty regexes...
    matchedKanji = re.search('<tr class="odd" >\\n\\t\\t\\t<td class="kanji_column">\\n\\t\\t\\t\\t<span class="kanji" style="z-index:\s\d+;"><span class="match">(.+)</span>\\t\\t\\t\\t</span>\\n\\t\\t\\t</td>\\n\\t\\t\\t<td class="kana_column">(.+)\\t\\t\\t</td>\\n\\t\\t\\t<td class="meanings_column">(.+)\\t\\t\\t</td>\\n\\t\\t</tr>', html)

    matchedKana = re.search('<tr class="odd" >\\n\\t\\t\\t<td class="kanji_column">\\n\\t\\t\\t\\t<span class="kanji" style="z-index: .+;">(.+)\\t\\t\\t\\t</span>\\n\\t\\t\\t</td>\\n\\t\\t\\t<td class="kana_column"><span class="match">(.+)</span>\\t\\t\\t</td>\\n\\t\\t\\t<td class="meanings_column">(.+)\\t\\t\\t</td>\\n\\t\\t</tr>', html)

    if matchedKanji:
        kanji = matchedKanji.groups()[0]
        if word != kanji:
            return word

        kana = matchedKanji.groups()[1]
        english = matchedKanji.groups()[2]

        english = engDefFix(english)

        if len(english) > 45:
            english = english[0:46]

        returnString = kanji+"\t\t"+kana+"\t\t"+english
        return returnString

    elif matchedKana:
        kanji = matchedKana.groups()[0] 
        kana = matchedKana.groups()[1]
        if word != kana:
            return word

        english = matchedKana.groups()[2]

        english = engDefFix(english)

        if len(english) > 45:
            english = english[0:46]

        returnString = kanji+"\t\t"+kana+"\t\t"+english
        return returnString

    else:
        return word


#/* Helper functions */

def engDefFix(word):
    newWord = removeTag(word, '<strong>')
    newWord = removeTag(newWord, '</strong>')
    newWord = removeTag(newWord, '<br>')
    newWord = removeTag(newWord, '</br>')
    newWord = removeTag(newWord, '<br />')

    return newWord


def removeTag(word, tag):
    splitGroups = word.split(tag)
    fixed = ''
    for item in splitGroups:
        fixed = fixed + item
    return fixed

def fixLine(line):
    #print "line: '" + line +"'"
    noNewLine = re.search('(.+)', line)
    nextLine = noNewLine.string[noNewLine.start():noNewLine.end()]
    nextLine = nextLine.split("　")[0]
    nextLine = nextLine.split()[0]
    return nextLine


if __name__ == "__main__":
    main()
