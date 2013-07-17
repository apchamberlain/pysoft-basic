#!/usr/local/bin/python

#  Microsoft BASIC clone in Python 2.7

#  Copyright (C) 2013  Alexander Park Chamberlain

#  Author: Alex Chamberlain <apchamberlain@gmail.com>
#  Version: 0.1
#  Package-Requires: pyparsing 1.5.7
#  "pip install -Iv http://sourceforge.net/projects/pyparsing/files/pyparsing/pyparsing-1.5.7/pyparsing-1.5.7.tar.gz/download"

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

#  pysoft-basic/parser.py: parsing routines and unit tests

#  This file is meant to be imported by pysoft-basic.py.  Run standalone
#  to execute unit tests.



from pyparsing import Literal,Word,ZeroOrMore,Forward,nums,oneOf,Group,\
    Combine,Suppress,printables,Optional,srange,operatorPrecedence,opAssoc

import unittest




class InputLine:
    class _Parser:

        linenum = Word(nums)
        string_literal = Combine(Suppress('"') + Word(printables + ' ') \
                                 + Suppress('"'))
        floatnum = Combine(Optional(oneOf('+ -')) \
                           + Word(nums) + Optional('.') \
                           + Optional(Word(nums))) \
                           ("flt") \
                           .setParseAction(lambda string, where, tokens: \
                                           [float(tokens[0])] )
        variable = Word(srange("[A-Z_]")) # FIXME: this is only for numeric vars
        operand = floatnum | variable
        powop = Literal('^')
        signop = oneOf('+ -')
        multop = oneOf('* /')
        plusop = oneOf('+ -')
        # TODO: unary functions like SIN, ABS, etc. go here.
        arith_expr = operatorPrecedence(operand,
                                        [(powop, 2, opAssoc.RIGHT),
                                         (signop, 1, opAssoc.RIGHT),
                                         (multop, 2, opAssoc.LEFT),
                                         (plusop, 2, opAssoc.LEFT), ]
                                        )  # TODO: how to combine operatorPrecedence()
                                           # with Forward() to nest expressions?
        bool_op = oneOf('= <> < >')
        # TODO: use operatorPrecedence and define AND, OR, NOT
        bool_expr = (floatnum | variable | arith_expr) \
            + bool_op + (floatnum | variable | arith_expr)

        assign_stmt = variable('lvar') + '=' + arith_expr('rvar')
        print_stmt = "PRINT" + variable('printvar') | arith_expr('printexpr') \
            | string_literal('printstring')
        goto_stmt = "GOTO" + linenum('dest')
        if_stmt = "IF" + bool_expr('condition') + "THEN GOTO" + linenum('dest')
        # TODO: stmt needs to be forward-defined so that
        # anything, not just a GOTO, can follow an IF
        # TODO: all other statements!
        run_cmd = "RUN" + Optional(linenum)('dest')
        list_cmd = "LIST"
        save_cmd = "SAVE" + string_literal("filespec")
        load_cmd = "LOAD" + string_literal("filespec")

        command = run_cmd | list_cmd | save_cmd | load_cmd
        immediate_line = assign_stmt | print_stmt | command
        stmt = assign_stmt | print_stmt | goto_stmt | if_stmt  #| other kinds of statements 
        program_line = linenum('linenum') + stmt('stmt')
        
        input_line = program_line('program_line') \
            | immediate_line('immediate_line')

    def __init__(self, l):
        self._parsed = self._Parser.input_line.parseString(l, parseAll=True)

    def getParseResults(self):
        return self._parsed

    def __call__(self):
        

class TestPyBASICParser(unittest.TestCase):

    # def setUp(self):
    #     return

    def test_assignment_stmt(self):
        """Test parsing of a simple assignment statement.
        """
        string = "A = 3.14"
        test = InputLine(string)
        # self.AssertEqual(test.getParseResults().asList(), ['A', '=', 3.14])
        self.failUnlessEqual(test.getParseResults().asList(), ['A', '=', 3.14])
        # TODO: Investigate why the AssertEqual() method shows up when
        # I type "help(unittest.TestCase)" in the console but doesn't
        # seem to be inherited from TestCase while the deprecated
        # failUnlessEqual() is.

    def test_assignment_with_arith_expression(self):
        """Test parsing of an assignment with a simple arithmetic expression.
        """
        string = "A = 9 * NUM"
        test = InputLine(string)
        self.failUnlessEqual(test.getParseResults().asList(), ['A', '=', [9, '*', 'NUM']])

    def test_assignment_with_nested_arith_expression(self):
        """Test parsing of an assignment with a nested arithmetic expression.
        """
        string = "A = 9 + 2 + 3 * NUM"
        test = InputLine(string)
        self.failUnlessEqual(test.getParseResults().asList(), ['A', '=', [9, '+', 2, '+', [3, '*', 'NUM']]])

    def test_print_stmt(self):
        """Test parsing of an immediate-mode print statement with just a variable on the right.
        """
        string = "PRINT A"
        test = InputLine(string)
        self.failUnlessEqual(test.getParseResults().asList(), ['PRINT', 'A'])


def main():
    unittest.main()


if __name__ == '__main__':
    main()
