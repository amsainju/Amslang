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

    def check(self,ltype):
        return self.pending.getLextype() == ltype

    def advance(self):
        old = self.pending
        self.pending = self.oLexer.lex()
        return old

    def match(self,ltype):
        self.matchNoAdvance(ltype)
        return self.advance()

    def matchNoAdvance(self,ltype):
        if not (self.check(ltype)):
            print("Error in Line Number ",self.oLexer.lineNumber)
            sys.exit()

    def program(self):
        if(self.check(types.NEWLINE)):
            self.advance()
            self.program()
        self.getStatement()
        if not (self.check(types.END_OF_FILE)):
            self.match(types.NEWLINE)       #think about keeping this or replacing with semi-colon
        if (self.statementPending()):
            self.program()

    def getStatement(self):
        if (self.ifStatementPending()):
            return getIfStatement()
        elif (self.whileStatementPending()):
            return getwhileStatement()
        elif (self.functionDefPending()):
            return self.getFunctionDef()
        elif (self.idPending()):
            idname = self.match(types.ID)
            self.match(types.ASSIGN)
            if(self.check(types.OSQBRACE)): #Array Defination
                self.match(types.OSQBRACE)
                newarray = lexer.lexeme(types.ARRAY,None)
                optArrayItems = self.getOptArrayItems()
                self.match(types.CSQBRACE)
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
                expr = self.getExpression()
                idname.left = expr
                return idname
            elif (self.check(types.DOT)):
                self.match(types.DOT)
                if(self.check(types.FIND)):
                    self.match(types.OPAREN)
                    findexpression = self.getExpression()
                    self.match(types.CPAREN)
                    return self.cons(types.DICTIONARYSEARCH,idname,findexpression)
                if(self.check(types.APPEND)):
                    self.match(types.OPAREN)
                    findexpression = self.getExpression()
                    self.match(types.CPAREN)
                    return self.cons(types.ARRAYAPPEND,idname,findexpression)
            return idname
        elif (self.check(types.PRINT)):
            printexpr = self.match(types.PRINT)
            self.match(types.OPAREN)
            optArglist = getOptArgumentList()
            printexpr.left = optArglist
            return printexpr


    def getIfStatement(self):
        ifstatement = self.match(types.IF)
        self.match(types.OPAREN)
        expr = self.getExpression()
        self.match(types.CPAREN)
        self.match(types.OBRACE)
        block = self.getBlock()
        self.match(types.CBRACE)
        ifstatement.left = expr  
        expr.left = block
        if (self.elsePending()):
            elsecase = self.match(types.ELSE)
            if(self.ifStatementPending()):
                elsecase.left = self.getIfStatement()
                ifstatement.right = elsecase
                return ifstatement
            elif (self.blockPending()):
                self.match(types.OBRACE)
                elseblock = self.getBlock()
                self.match(types.CBRACE)
                elsecase.left = elseblock
                ifstatement.right = elsecase
                return ifstatement
        ifstatement.right = None
        return ifstatement

    def getWhileStatement(self):
        whilestatement = self.match(types.WHILE)
        self.match(types.OPAREN)
        expr = self.getExpression()
        self.match(types.CPAREN)
        self.match(types.OBRACE)
        block = self.getBlock()
        self.match(types.CBRACE)
        whilestatement.left = expr
        #expr.left = block
        #or
        whilestatement.right = block
        return whilestatement
 
#start here : 2016/3/4
    def getFunctionDef(self):
        self.match(types.DEFINE)
        functionName = self.match(types.ID)
        self.match(types.OPAREN)
        optParameterList = self.getOptIdentifierList()
        self.match(types.CPAREN)
        self.match(types.OBRACE)
        block = self.getBlock()
        self.match(types.CBRACE)
        functionName.left = optParameterList
        optParameterList.left = block
        return self.cons(types.FUNCDEF,functionName,(self.cons(types.JOIN, optParameterList, self.cons(types.JOIN,block,None))))


    def getOptIdentifierList(self):
        if(self.idPending()):
            return self.getIdentifierList()
        elif (self.check(types.CPAREN)):
            return lexer.lexeme(types.PARAMETERLIST,None)

    def getIdentifierList(self):
        a = self.match(types.ID)
        if (self.check(types.COMMA)):
            self.advance()
            b = self.getIdentifierList()
        else:
            b = None
        return self.cons(types.PARAMETERLIST,a,b)



    def getOptArgumentList(self):
        if(self.expressionPending()):
            return self.getArgumentList()
        elif (self.check(types.CPAREN)):
            return lexer.lexeme(types.ARGUMENTLIST,None)

    def getArgumentList(self):
        a = self.getExpression()
        if (self.check(types.COMMA)):
            self.advance()
            b = self.getArgumentList()
        else:
            b = None
        return self.cons(types.ARGUMENTLIST,a,b)


    def getExpression(self):
        a = self.getPrimary()
        if(self.opPending()):
            b = self.getOP()
            c = self.getExpression()
            b.left = a
            a.left = c
            return b
        else:
            return a

    def getPrimary(self):
        if (self.idPending()):
            idname = self.match(types.ID)
            if (self.check(types.OPAREN)):   #for function call
                self.match(types.OPAREN)
                optArgList = self.getArgumentList()
                self.match(types.CPAREN)
                return self.cons(types.FUNCTIONCALL,idname,optArgList)
            elif (self.check(types.OSQBRACE)):
                self.match(types.OSQBRACE)
                expr = getExpression()
                self.match(types.CSQBRACE)
                return self.cons(type.COLLECTIONACCESS,idname,expr)
            else:
                return idname
        elif (self.stringPending()):
            return self.match(types.STRING)
        elif (self.integerPending()):
            return self.match(types.INTEGER)
        elif (self.lambdaPending()):
            return self.getlambda()
        elif (self.check(types.MINUS)):
            sign = self.match(types.MINUS)
            value = self.getPrimary()
            sign.left = value
            return sign
        elif (self.check(types.OPAREN)):
            self.match(types.OPAREN)
            expr = self.getExpression()
            self.match(types.CPAREN)
            return expr

    def getlambda(self):
        self.match(types.LAMBDA)
        self.match(types.OPAREN)
        optIdList = self.getOptIdentifierList()
        self.match(types.CPAREN)
        self.match(types.COLON)
        self.match(types.OPAREN)
        expr = self.getExpression()
        self.match(types.CPAREN)
        if (self.check(types.OPAREN)):
            self.match(types.OPAREN)
            arglist = self.getArgumentList()
            self.match(type.CPAREN)
            return self.cons(types.CLOSURE,optIdList,self.cons(types.JOIN,expr,self.cons(types.JOIN,arglist,None)));
        else:
            return self.cons(types.CLOSURE,optIdList,self.cons(types.JOIN,expr,None));

    def getBlock(self):
        statement = self.getStatement()
        self.match(types.NEWLINE)
        if (self.statementPending()):
            statement2 = self.getBlock()
            return self.cons(types.STATEMENT,statement,statement2)
        else:
            return self.cons(types.STATEMENT,statment,None)


    def getOptArrayItems(self):
        if (self.arrayItemsPending()):
            return self.getArrayItems()
        elif (self.check(types.CSQBRACE)):
            return self.cons(types.ARRAYITEMS,None,None)

    def getOptDictItems(self):
        if (self.dictItemsPending()):
            return self.getDictItems()
        elif (self.check(types.CBRACE)):
            return self.cons(types.DICTIONARYITEMS,None,None)

    def getArrayItems(self):
        a = self.getPrimary()
        if (self.check(types.COMMA)):
            self.advance()
            b = self.getArrayItems()
            return self.cons(types.ARRAYITEMS,a,b)
        else:
            return self.cons(types.ARRAYITEMS,a,None)

    def getDictItems(self):
        a = self.getPrimary()
        col = self.match(types.COLON)    
        b = self.getPrimary()
        a.left = b
        if (self.check(types.COMMA)):
            self.advance()
            c = self.getDictItems()
            return self.cons(types.DICTIONARYITEMS,a,c)
        else:
            return self.cons(types.DICTIONARYITEMS,a,None)

    def getOP(self):
        if(self.check(types.PLUS)):
            return self.match(types.PLUS)
        elif(self.check(types.MINUS)):
            return self.match(types.MINUS)
        elif(self.check(types.DIVIDE)):
            return self.match(types.DIVIDE)
        elif(self.check(types.TIMES)):
            return self.match(types.TIMES)
        elif(self.check(types.MOD)):
            return self.match(types.MOD)
        elif(self.check(types.ASSIGN)):
            return self.match(types.ASSIGN)
        elif(self.check(types.GREATERTHAN)):
            return self.match(types.GREATERTHAN)
        elif(self.check(types.GREATERTHANEQUALTO)):
            return self.match(types.GREATERTHANEQUALTO)
        elif(self.check(types.LESSTHAN)):
            return self.match(types.LESSTHAN)
        elif(self.check(types.LESSTHANEQUALTO)):
            return self.match(types.LESSTHANEQUALTO)
        elif(self.check(types.OR)):
            return self.match(types.OR)
        elif(self.check(types.AND)):
            return self.match(types.AND)

    def cons(self,ltype,leftlexeme,rightlexeme):
        intermediate = lexer.lexeme(ltype,None)
        intermediate.left = leftlexeme
        intermediate.right = rightlexeme
        return intermediate


    def opPending(self):
        return self.check(types.PLUS) or self.check(types.MINUS) or self.check(types.DIVIDE) or self.check(types.TIMES) or self.check(types.MOD) or self.check(types.GREATERTHAN) or self.check(types.GREATERTHANEQUALTO) or self.check(types.LESSTHAN) or self.check(types.LESSTHANEQUALTO) or self.check(types.EQUALTO) or self.check(types.OR) or self.check(types.AND)


    def elsePending(self):
        return self.check(types.ELSE)

    def blockPending(self):
        return self.check(types.OBRACE)

    def dictItemsPending():
        return self.primaryPending()


    def statementPending(self):
        return self.ifStatementPending() or self.whileStatementPending() or self.functionDefPending() or self.idPending()

    def arrayItemsPending(self):
        return self.primaryPending()

    def idPending(self):
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
        return self.idPending() or self.stringPending() or self.integerPending() or self.lambdaPending() or self.minusPending() or self.check(types.OPAREN)

    def stringPending(self):
        return self.check(types.STRING)

    def integerPending(self):
        return self.check(types.INTEGER)

    def lambdaPending(self):
        return self.check(types.LAMBDA)

    def minusPending(self):
        return self.check(types.MINUS)






