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
        self.getStatement()
        self.match(types.NEWLINE)       #think about keeping this or replacing with semi-colon
        if (self.statementPending()):
            self.program()

    def getStatement(self):
        if (self.ifStatementPending()):
            return getIfStatement()
        elif (self.whileStatementPending()):
            return getwhileStatement()
        elif (self.functionDefPending()):
            return getFunctionDef()
        elif (self.idPending()):
            idname = self.match(types.ID)
            self.match(types.ASSIGN)
            if(self.check(types.OSBRACE)): #Array Defination
                self.match(types.OSBRACE)
                newarray = lexer.lexeme(types.ARRAY,None)
                optArrayItems = self.getOptArrayItems()
                self.match(types.CSBRACE)
                newarray.left = optArrayItems
                idname.left = newarray
                return idname
             elif (self.check(types.OBRACE)): #Dictionary defination
                self.match(types.OBRACE)
                optDictItems = self.getOptDictItems()
                self.match(type.CBRACE)
                newdict = lexer.lexeme(types.DICTIONARY,None)
                newdict.left = optDictItems
                idname.left = newdict
                return idname
            elif (self.expressionPending()):   #variable decleration and defination and update
                expr = getExpression()
                idname.left =expr
                return idname

    def getIfStatement(self):
        ifstatement = self.match(types.IF)
        self.match(types.OPAREN)
        expr = self.getExpression()
        self.match(types.CPAREN)
        block = self.getBlock()
        ifstatement.left = expr  
        expr.left = block
        if (self.elsePending()):
            elsecase = self.match(types.ELSE)
            if(self.ifStatementPending()):
                elsecase.left = self.getIfStatement()
                ifstatement.right = elsecase
                return ifstatement
            elif (self.blockPending()):
                elseblock = self.getBlock()
                elsecase.left = elseblock
                return ifstatement.right = elsecase
                return ifstatement
        ifstatement.right = None
        return ifstatement

    def getWhileStatement(self):
        whilestatement = self.match(types.WHILE)
        self.match(types.OPAREN)
        expr = self.getExpression()
        self.match(types.CBRACE)
        block = self.getBlock()
        whilestatement.left = expr
        expr.left = block
        return whilestatement
 
#start here : 2016/3/4
    def getFunctionDef(self):
        self.match(types.DEFINE)
        functionName = self.match(types.ID)
        self.match(types.OPAREN)
        optParameterList = self.getOptIdentifierList()
        self.match(types.CPAREN)
        block = self.getBlock()
        #think to return the combination of function name
        #argumentlist
        #and body

    def getOptIdentifierList(self):
        if(self.identifierListPending()):
            return self.getIdentifierList()
        elif (self.check(types.CPAREN)):
            return None

    def getIdentifierList(self):
        a = self.match(types.ID)
        if (self.check(types.COMMA)):
            self.advance()
            b = self.getIdentifierList()
            #return combinationa of a and b
        else:
            return a


    def getExpression(self):
        a = self.getPrimary()
        if(self.opPending()):
            b = self.getOP()
            c = getExpression()
            b.left = a
            a.left = c
            return b
        else:
            return a

    def getPrimary(self):
        if (self.idPending()):
            idname = self.match(types.ID)
            if (self.check(types.OPAREN)):
                self.match(types.OPAREN)
                optArgList = self.getArgumentList()
                self.match(types.CPAREN)
                #return something
            elif (self.check(types.OSBRACE)):
                self.match(types.OSBRACE)
                expr = getExpression()
                self.match(types.CSBRACE)
                #return something
            else:
                return idname
        elif (self.stringPending()):
            return self.match(types.STRING)
        elif (self.integerPending()):
            return self.match(types.INTEGER)
        elif (self.lambdaPending()):
            lam = self.match(types.LAMBDA)
            self.match(types.OPAREN)
            optIdList = self.getOptIdentifierList()
            self.match(types.CPAREN)
            self.match(types.COLON)
            self.match(types.OPAREN)
            expr = self.getExpression()
            self.match(types.CPAREN) # i think argument list is not required here not added argument list 
            #return combination of idlist and body
        elif (self.check(types.MINUS)):
            sign = self.match(types.MINUS)
            value = self.getPrimary()
            #do some thing

    def getBlock(self):
        self.match(types.OBRACE)
        statementlist = None
        if (self.statementPending()):
            statementlist = self.getStatementList()
        self.match(types.CBRACE)
        return statementlist

    def getStatementList(self):
        statement = self.getStatement()
        self.match(types.NEWLINE)
        if(self.statementPending()):
            statement2 = self.getStatementList()
            return #something
        else:
            return statement




    def getOptArrayItems(self):
        if (self.arrayItemsPending()):
            return self.getArrayItems()
        elif (self.check(types.CSBRACE)):
            return None

    def getOptDictItems(self):
        if (self.dictItemsPending()):
            return self.getDictItems()
        elif (self.check(types.CBRACE)):
            return None

    def getArrayItems(self):
        a = self.getPrimary()
        b = None
        if (self.check(types.COMMA)):
            self.advance()
            b = self.getArrayItems()
        return self.cons(ARRAYITEMS,a,b)

    def getDictItems(self):
        a = self.getPrimary()
        col = self.match(types.COLON)    
        b = self.getPrimary()
        c = lexer.lexeme(None,None)
        c.left = a
        c.right = b
        if (self.check(types.COMMA)):
            self.advance()
            d = self.getDictItems()
        return self.cons(DICTITEMS,c,d)

    def opPending(self):
        return self.check(types.MINUS) or self.check(types.DIVIDE) or self.check(types.TIMES) or self.check(types.MOD) or self.check(types.GREATERTHAN) or self.check(types.GREATERTHANEQUALTO) or self.check(types.LESSTHAN) or self.check(types.LESSTHANEQUALTO) or self.check(types.EQUALTO) or self.check(types.OR) or self.check(types.AND)


    def elsePending(self):
        return self.check(types.ELSE)

    def blockPending(self):
        return self.check(types.OBRACE)

    def dictItemsPending():
        return self.primaryPending()


    def statementPending(self):
        return self.ifStatementPending() or self.whileStatementPending() or self.functionDefPending() or self.idPending)

    def arrayItemsPending(self):
        return self.primaryPending()

    def idPending():
        return self.check(types.ID)

    def ifStatementPending(self):
        return self.check(types.IF)

    def whileStatementPending(self):
        return self.check(types.WHILE)

    def functionDefPending(self):
        return self.check(types.DEFINE)

    def expressionPending(self):
        return self.primaryPending()

    def primaryPending(self):
        return self.idPending() or self.stringPending() or self.integerPending() or self.lambdaPending() or self.minusPending()

    def stringPending(self):
        return self.check(types.STRING)

    def integerPending(self):
        return self.check(types.INTEGER)

    def lambdaPending(self):
        return self.check(types.LAMBDA)

    def minusPending(self):
        return self.check(types.MINUS)






