# csc521
Homework1


This Assignment was to write a Lexer, Parser, and Interpreter for Quirk Programming Language Developed by Josh Mccoy at AU


I am using Python 3.5

To run a quirk file simpley go to you command line and type in the following command

python Lexer.py <"YOURFILE".q | Parser.py | Interpreter.py

The command line will output your output of your quirk program

If you want to just do python Lexer.py <YourFile.q

Look for Comments in the Program in method getDemStringsAndLiterals()
It should be very obvious where it is.

If you want to print out the parse tree in Parser.py by running python Parser.py <YourFile.q
Then again You must Look for printing instructions in main

All these instructions are at the bottom of the Programs and I have made them extremely Clear.


Homework 2

Clojure Interpreter

This assignment was to create a parse tree, and to interpret it through left depth first search algorithm in the programming language
Clojure.

To run a quirk file on the command line simply type in lein run <"YourFile".q 

To output only a parse tree type on command line,   lein run -pt <"Yourfile".q
This command will not output the output of the quirk file only the corresponding parse tree
 
All 5 examples are working, but there are obvious bugs if you go outside the normal examples
Although in Example 5 you may try to return any of the 3 Values that does work.

