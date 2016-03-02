#Author: Arpan Man Sainju
#Date: 
#Description: 
import lexer 
import sys
from type import types
class cparser:
    def __init__(self,source):
        self.source = source
        self.pending = lexer.lexeme(None,None)
        
    def parser(self):
        self.oLexer = lexer.lexer(self.source)
        self.pending = self.oLexer.lex()
        self.program()
        self.match(types.END_OF_FILE)    
        while(self.pending.getLextype()!= types.END_OF_FILE):
            if(self.pending.getLextype() != types.BADCHARACTER):
               print(self.pending.getLextype(), end= ' ')
               if(self.pending.getLexval() != None):
                   print(self.pending.getLexval())
               else:
                   print()
            else:
               print("Error in Line Number ", lexer.lexer.lineNumber,". Unknown character ","'",self.pending.getLexval(),"'.")
               break
            self.pending = self.oLexer.lex()
        print("End of Program")

    def check(self,type):
        return self.pending.getLextype == type

    def advance(self):
        old = self.pending
        self.pending = self.oLexer.lex()
        return old

    def match(self,type):
        self.matchNoAdvance(type)
        self.advance()

    def matchNoAdvance(self,type):
        if not (self.check(type)):
            print("Error in Line Number ",self.oLexer.lineNumber)
            sys.exit()

    def program(self):
        self.statement()
        if (self.statementPending()):
            self.program()

    def statement(self):
        if (self.ifStatementPending()):
            return ifStatement()
        elif (self.whileStatementPending()):
            return whileStatement()
        elif (self.functionDefPending()):
            return functionDef()
        elif (self.idPending()):
            idname = self.match(types.ID)
            self.match(types.ASSIGN)
            if(self.check(types.OSBRACE)): #Array Defination
                self.match(types.OSBRACE)
                optArrayItems = self.getOptArrayItems()
                self.match(types.CSBRACE)
                #DO SOME KIND OF COMBINATION BETWEEN ID NAME AND OPTARRAYITEMS
            elif (self.check(types.OBRACE)):
                self.match(types.OBRACE)
                optDictItems = self.getOptDictItems()
                self.match(type.CBRACE)
                #join and return
            elif (self.expressionPending()):
                expr = expression()
                #join and returnz



        
    def statementPending(self):
        return self.ifStatementPending() or self.whileStatementPending() or self.functionDefPending() or self.idPending)

