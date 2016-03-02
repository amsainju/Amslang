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
        while(self.pending.getLextype()!= types.END_OF_FILE):
            #print(lexer.lexer.lineNumber)
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