import re
import itertools
import sys
Lexemes = {"(": "LPAREN",
           ")": "RPAREN",
           ",": "COMMA",
           ":": "COLON",
           "function": "FUNCTION",
           "{": "LBRACE",
           "}": "RBRACE",
           "+": "ADD",
           "-": "SUB",
           "*": "MULT",
           "/": "DIV",
           "^": "EXP",
           "var": "VAR",
           "return": "RETURN",
           "print": "PRINT",
           "=": "ASSIGN"}

UpperLexemes = {"LPAREN", "RPAREN", "COMMA", "COLON",
                "FUNCTION", "LBRACE", "RBRACE", "ADD",
                "SUB", "MULT", "DIV", "EXP", "VAR", "RETURN",
                "PRINT", "ASSIGN"}


def stripLexemes(source):
    '''
    Purpose of this Function is to split by character
    This will allow for ex. such as   12+2 to easily
    become 12 ADD 2
    '''
    noLexemeString = list(source)
    myArray2 = []
    t = 0
    k = 0
    while t < len(noLexemeString):
        temp = noLexemeString[t]
        for lexeme in Lexemes:
            if temp == lexeme:
                temp = " " + Lexemes[temp] + " "
                noLexemeString[t] = temp
        t = t+1
    myArray2 = list(itertools.chain(*noLexemeString))
    newString = "".join(noLexemeString)
    return newString


def stripWhiteSpace(source):
    '''
    After Split by Char, Now can Split by White space
    Take Care of other Elements
    '''
    noWhiteString = source.split()
    myArray = []
    i = 0
    while i < len(noWhiteString):
        temp = noWhiteString[i]
        for lexeme in Lexemes:
            if temp == lexeme:
                temp = Lexemes[temp]
                noWhiteString[i] = " " + temp + " "
            else:
                noWhiteString[i] = " " + temp + " "
        i = i+1
    stringToPass = "  ".join(noWhiteString)
    return stringToPass


def getDemNumbersAndLiterals(source):
    '''
    Gotta use that Regex to make sure things are
    Valid Numbers and Strings(names)
    '''
    regexNumber = r"(((\d+(\.\d*)?)|(\.\d+)))"
    regexIdent = r"([a-zA-Z]+[a-zA-Z0-9_]*)"
    stringGiven = source.split()
    i = 0
    myArray = []
    while i < len(stringGiven):
        temp = stringGiven[i]
        tokenFound = False
        for lexeme in UpperLexemes:
            if temp == lexeme:
                tokenFound = True
                myArray.append(temp)
        if not tokenFound:
            if (re.search(regexNumber, temp)):
                temp2 = "NUMBER:" + str(temp)
                myArray.append(temp2)
            if(re.search(regexIdent, temp)):
                temp2 = "IDENT:" + str(temp)
                myArray.append(temp2)
        i = i+1
    myArray.append('EOF')
    '''
    UNCOMMENT BOTTOM 2 LINES IF YOU WANT
    IT TO PRINT OUT NICE
    '''
    '''
    for i in range(len(myArray)):
        print(myArray[i])
    '''
    return (myArray)

def ReadInput():
    '''
        Reading File
        '''
    lines = sys.stdin.readlines()
    return lines

if __name__ == '__main__':
    myList = ''.join(ReadInput())
    LexedList = getDemNumbersAndLiterals(stripWhiteSpace(stripLexemes(myList)))
    # Comment Out below if you want to run just python Lexer.py <YourFile
    # Also look for uncommenting Instructions above
    sys.stdout.write(str(LexedList))
