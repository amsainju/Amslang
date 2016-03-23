#Author: Arpan Man Sainju
#Date: 
#Description: 
import lexer 
import sys
import helper
from type import types
class cparser:
    def __init__(self,source):
        self.source = source
        self.pending = lexer.lexeme(None,None)
        
    def parser(self):
        self.oLexer = lexer.lexer(self.source)
        self.pending = self.oLexer.lex()
        parsetree = self.program()
        self.match(types.END_OF_FILE)
        retrun parsetree   
        #print("End of Program")

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
            #print("Error in Line Number ",self.oLexer.lineNumber, "Expecting: ",ltype, "Got TYPE: ", self.pending.getLextype(), "Got Value: ",self.pending.getLexval())
            print("Error in Line Number ",self.oLexer.lineNumber, "Expecting: ",ltype, "Got TYPE: ", self.pending.getLextype())
            sys.exit()

    def program(self):
        stmt = self.getStatement()
        if (self.statementPending()):
            stmt2 = self.program()
            return helper.cons(types.JOIN,stmt,stmt2)
        else:
            return stmt

    def getStatement(self):
        if (self.ifStatementPending()):
            return self.getIfStatement()
        elif (self.whileStatementPending()):
            return self.getWhileStatement()
        elif (self.functionDefPending()):
            return self.getFunctionDef()
        if(self.idPending()):
            idname = self.match(types.ID)
            if (self.check(types.ASSIGN)):
                self.match(types.ASSIGN)
                if(self.check(types.OSQBRACE)): #Array Defination
                    self.match(types.OSQBRACE)
                    newarray = lexer.lexeme(types.ARRAY,None)
                    optArrayItems = self.getOptArrayItems()
                    self.match(types.CSQBRACE)
                    newarray.left = optArrayItems
                    idname.left = newarray
                    self.match(types.SEMI)
                    return idname
                elif (self.check(types.OBRACE)): #Dictionary defination
                    self.match(types.OBRACE)
                    optDictItems = self.getOptDictItems()
                    self.match(types.CBRACE)
                    newdict = lexer.lexeme(types.DICTIONARY,None)
                    newdict.left = optDictItems
                    idname.left = newdict
                    self.match(types.SEMI)
                    return idname
                elif (self.check(types.INPUT)):
                    inputcommand = self.match(types.INPUT)
                    self.match(types.OPAREN)
                    msg = self.getPrimary()
                    self.match(types.CPAREN)
                    self.match(types.SEMI)
                    inputcommand.left = msg
                    idname.left = inputcommand
                    return idname
                elif (self.expressionPending()):   #variable decleration and defination and update
                    expr = self.getExpression(None)
                    idname.left = expr
                    self.match(types.SEMI)
                    return idname
            elif (self.check(types.OSQBRACE)):    #Array or Dictionary update
                self.match(types.OSQBRACE);
                expr = self.getExpression(None)
                self.match(types.CSQBRACE)
                self.match(types.ASSIGN)
                expr2= self.getExpression(None)
                self.match(types.SEMI)
                return helper.cons(types.COLLECTIONUPDATE,idname,helper.cons(types.JOIN,expr, helper.cons(types.JOIN, expr2,None)))
            else:
                expr =  self.getExpression(idname)
                self.match(types.SEMI)
                return expr
        elif (self.check(types.PRINT)):
            printexpr = self.match(types.PRINT)
            self.match(types.OPAREN)
            optArglist = self.getOptArgumentList()
            self.match(types.CPAREN)
            printexpr.left = optArglist
            self.match(types.SEMI)
            return printexpr

        else:
            expr = self.getExpression(None)
            self.match(types.SEMI)
            return expr


    def getIfStatement(self):
        ifstatement = self.match(types.IF)
        self.match(types.OPAREN)
        expr = self.getExpression(None)
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
        expr = self.getExpression(None)
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
        return helper.cons(types.FUNCDEF,functionName,(helper.cons(types.JOIN, optParameterList, helper.cons(types.JOIN,block,None))))


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
        return helper.cons(types.PARAMETERLIST,a,b)



    def getOptArgumentList(self):
        if(self.expressionPending()):
            return self.getArgumentList()
        elif (self.check(types.CPAREN)):
            return lexer.lexeme(types.ARGUMENTLIST,None)

    def getArgumentList(self):
        a = self.getExpression(None)
        if (self.check(types.COMMA)):
            self.advance()
            b = self.getArgumentList()
        else:
            b = None
        return helper.cons(types.ARGUMENTLIST,a,b)


    def getExpression(self,first):
        if(first):
            a = first
        else:
            a = self.getPrimary()
        if(self.opPending()):
            b = self.getOP()
            c = self.getExpression(None)
            if (c == None):
                print("Error in LineNumber:", self.oLexer.lineNumber,"Expecting an Expression after", b.getLextype())
                sys.exit()
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
                return helper.cons(types.FUNCTIONCALL,idname,optArgList)
            elif (self.check(types.OSQBRACE)):
                self.match(types.OSQBRACE)
                expr = self.getExpression(None)
                self.match(types.CSQBRACE)
                return helper.cons(types.COLLECTIONACCESS,idname,expr)
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
            expr = self.getExpression(None)
            self.match(types.CPAREN)
            return expr
        else:
            return None

    def getlambda(self):
        self.match(types.LAMBDA)
        self.match(types.OPAREN)
        optIdList = self.getOptIdentifierList()
        self.match(types.CPAREN)
        self.match(types.COLON)
        self.match(types.OPAREN)
        expr = self.getExpression(None)
        self.match(types.CPAREN)
        if (self.check(types.OPAREN)):
            self.match(types.OPAREN)
            arglist = self.getArgumentList()
            self.match(types.CPAREN)
            return helper.cons(types.CLOSURE,optIdList,helper.cons(types.JOIN,expr,helper.cons(types.JOIN,arglist,None)));
        else:
            return helper.cons(types.CLOSURE,optIdList,helper.cons(types.JOIN,expr,None));

    def getBlock(self):
        statement = self.getStatement()
        #self.match(types.SEMI)
        if (self.statementPending()):
            statement2 = self.getBlock()
            return helper.cons(types.STATEMENT,statement,statement2)
        else:
            return helper.cons(types.STATEMENT,statement,None)


    def getOptArrayItems(self):
        if (self.arrayItemsPending()):
            return self.getArrayItems()
        elif (self.check(types.CSQBRACE)):
            return helper.cons(types.ARRAYITEMS,None,None)

    def getOptDictItems(self):
        if (self.dictItemsPending()):
            return self.getDictItems()
        elif (self.check(types.CBRACE)):
            return helper.cons(types.DICTIONARYITEMS,None,None)

    def getArrayItems(self):
        a = self.getPrimary()
        if (self.check(types.COMMA)):
            self.advance()
            b = self.getArrayItems()
            return helper.cons(types.ARRAYITEMS,a,b)
        else:
            return helper.cons(types.ARRAYITEMS,a,None)

    def getDictItems(self):
        a = self.getPrimary()
        col = self.match(types.COLON)    
        b = self.getPrimary()
        a.left = b
        if (self.check(types.COMMA)):
            self.advance()
            c = self.getDictItems()
            return helper.cons(types.DICTIONARYITEMS,a,c)
        else:
            return helper.cons(types.DICTIONARYITEMS,a,None)

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
        elif(self.check(types.EQUALTO)):
            return self.match(types.EQUALTO)
        elif(self.check(types.NOTEQUAL)):
            return self.match(types.NOTEQUAL)
        elif(self.check(types.OR)):
            return self.match(types.OR)
        elif(self.check(types.AND)):
            return self.match(types.AND)

    def opPending(self):
        return self.check(types.PLUS) or self.check(types.MINUS) or self.check(types.DIVIDE) or self.check(types.TIMES) or self.check(types.MOD) or self.check(types.GREATERTHAN) or self.check(types.GREATERTHANEQUALTO) or self.check(types.LESSTHAN) or self.check(types.LESSTHANEQUALTO) or self.check(types.EQUALTO)  or self.check(types.NOTEQUAL) or self.check(types.OR) or self.check(types.AND)


    def elsePending(self):
        return self.check(types.ELSE)

    def blockPending(self):
        return self.check(types.OBRACE)

    def dictItemsPending(self):
        return self.primaryPending()


    def statementPending(self):
        return self.ifStatementPending() or self.whileStatementPending() or self.functionDefPending() or self.idPending() or self.check(types.PRINT)

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






