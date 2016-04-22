#Author: Arpan Man Sainju
#Date: 03/10/2016
#Description: contains class cparser for parsing the lexemes 
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
        return parsetree   
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
            print("Error in Line Number ",self.oLexer.lineNumber, "Expecting: ",ltype, "Got : ", self.pending.getLextype())
            sys.exit()

    def program(self):
        stmt = self.getStatement()
        if (self.statementPending()):
            stmt2 = self.program()
            return helper.cons(types.STATEMENT,stmt,stmt2)
        else:
            return helper.cons(types.STATEMENT,stmt,None)

    def getStatement(self):
        if (self.ifStatementPending()):
            return self.getIfStatement()
        elif (self.whileStatementPending()):
            return self.getWhileStatement()
        elif (self.functionDefPending()):
            return self.getFunctionDef()
        elif (self.varPending()):
            return self.getVariableDefination()  
        else:
            expr = self.getExpression()
            self.match(types.SEMI)
            return expr

    def getVariableDefination(self):
        var = self.match(types.VAR)
        idname = self.match(types.ID)
        self.match(types.ASSIGN)
        if(self.check(types.OSQBRACE)): #Array Defination
            self.match(types.OSQBRACE)
            newarray = lexer.lexeme(types.ARRAY,None)
            optArrayItems = self.getOptArrayItems()
            self.match(types.CSQBRACE)
            newarray.left = optArrayItems
            self.match(types.SEMI)
            var.left = idname
            var.right = newarray
            return var
        else:
            expr = self.getExpression()
            self.match(types.SEMI)
            var.left = idname
            var.right = expr
            return var


    def getIfStatement(self):
        ifstatement = self.match(types.IF)
        self.match(types.OPAREN)
        expr = self.getExpression()
        self.match(types.CPAREN)
        self.match(types.OBRACE)
        block = self.getBlock()
        self.match(types.CBRACE)
        ifstatement.left = expr  
        ifstatement.right = helper.cons(types.JOIN,block,None)
        if (self.elsePending()):
            elsecase = self.match(types.ELSE)
            if(self.ifStatementPending()):
                elsecase.left = self.getIfStatement()
                ifstatement.right.right = elsecase
                return ifstatement
            elif (self.blockPending()):
                self.match(types.OBRACE)
                elseblock = self.getBlock()
                self.match(types.CBRACE)
                elsecase.left = elseblock
                ifstatement.right.right = elsecase
                return ifstatement
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
        pt = helper.cons(types.FUNCDEF,functionName,(helper.cons(types.JOIN, optParameterList, helper.cons(types.JOIN,block,None))))
        return pt


    def getOptIdentifierList(self):
        if(self.idPending()):
            return self.getIdentifierList()
        elif (self.check(types.CPAREN)):
            return lexer.lexeme(types.PARAMETERLIST,None)

    def getIdentifierList(self):
        if (self.check(types.OPAREN)):
            a = self.match(types.OPAREN)
            idname = self.match(types.ID)
            self.match(types.CPAREN)
            a.left = idname
        else:
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
        a = self.getExpression()
        if (self.check(types.COMMA)):
            self.advance()
            b = self.getArgumentList()
        else:
            b = None
        return helper.cons(types.ARGUMENTLIST,a,b)

    def getExpression(self):
        expr =self.getExpression1()
        if(self.comparisonPending()):
            comp = self.getComparison()
            expr2 = self.getExpression1()
            comp.left=expr
            comp.right= expr2
            if(self.gatePending()):
                gate = self.getGate()
                expr3 = self.getExpression()
                gate.left=comp
                gate.right=expr3
                return gate
            else:
                return comp
        else:
            return expr
            
    def getExpression1(self):
        a = self.getPrimary()
        if(a.getLextype()== "ID" or a.getLextype()=="COLLECTIONACCESS"):
            if(a.getLextype() == "COLLECTIONACCESS"):
                if(self.check(types.ASSIGN)):
                    self.match(types.ASSIGN)
                    expr = self.getExpression()
                    pos = a.right.right
                    idname = a.right.left
                    return helper.cons(types.COLLECTIONUPDATE,idname,helper.cons(types.JOIN,pos, helper.cons(types.JOIN, expr,None)))
            elif(a.getLextype()=="ID"):
                if(self.check(types.ASSIGN)):
                    assign = self.match(types.ASSIGN)
                    expr = self.getExpression()
                    assign.left = a
                    assign.right = expr
                    return assign
                if(self.check(types.DOT)):
                    self.match(types.DOT)
                    if(self.check(types.APPEND)):
                        self.match(types.APPEND)
                        self.match(types.OPAREN)
                        expr = self.getExpression()
                        self.match(types.CPAREN)
                        return helper.cons(types.ARRAYAPPEND,a,expr)
                    elif(self.idPending()):
                        variable = self.match(types.ID)
                        idname = a
                        a = helper.cons(types.DISPATCH,None,helper.cons(types.JOIN,idname,variable))
                        if (self.check(types.ASSIGN)):
                            self.match(types.ASSIGN)
                            expr = self.getExpression()
                            return helper.cons(types.DISPATCHASSIGN,idname,helper.cons(types.JOIN,variable,expr))
                    else:
                        helper.showerror("Error: Expecting ID got ",self.pending.getLextype())
        if(self.opPending()):
            b = self.getOP()
            c = self.getExpression1()
            if (c == None):
                helper.showerror("Error in LineNumber: "+ self.oLexer.lineNumber+" Expecting an Expression after "+ b.getLextype())
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
                optArgList = self.getOptArgumentList()
                self.match(types.CPAREN)
                return helper.cons(types.FUNCTIONCALL,None,helper.cons(types.JOIN,idname,optArgList))
            elif (self.check(types.OSQBRACE)):
                self.match(types.OSQBRACE)
                expr = self.getExpression()
                self.match(types.CSQBRACE)
                return helper.cons(types.COLLECTIONACCESS,None,helper.cons(types.JOIN,idname,expr))
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
            oparen = self.match(types.OPAREN)
            parenExpr = self.getExpression()
            self.match(types.CPAREN)
            oparen.right = parenExpr
            return oparen
        else:
            return None

    def getlambda(self):
        self.match(types.LAMBDA)
        self.match(types.OPAREN)
        optParameterList = self.getOptIdentifierList()
        self.match(types.CPAREN)
        self.match(types.OBRACE)
        block = self.getBlock()
        self.match(types.CBRACE)
        if (self.check(types.COLON)):
            self.match(types.COLON)
            self.match(types.OPAREN)
            arglist = self.getOptArgumentList()
            self.match(types.CPAREN)
            return helper.cons(types.LAMBDACALL,None,(helper.cons(types.JOIN,arglist, helper.cons(types.JOIN,optParameterList,helper.cons(types.JOIN,block,None)))))
        else:
            return helper.cons(types.LAMBDA,None,(helper.cons(types.JOIN, optParameterList, helper.cons(types.JOIN,block,None))))


    def getBlock(self):
        statement = self.getStatement()
        if (self.statementPending()):
            statement2 = self.getBlock()
            return helper.cons(types.STATEMENT,statement,statement2)
        else:
            return helper.cons(types.STATEMENT,statement,None)


    def getOptArrayItems(self):
        if (self.arrayItemsPending()):
            return self.getArrayItems()
        elif (self.check(types.CSQBRACE)):
            return helper.cons(types.JOIN,None,None)

    def getOptDictItems(self):
        if (self.dictItemsPending()):
            return self.getDictItems()
        elif (self.check(types.CBRACE)):
            return helper.cons(types.JOIN,None,None)

    def getArrayItems(self):
        a = self.getExpression()
        if (self.check(types.COMMA)):
            self.advance()
            b = self.getArrayItems()
            return helper.cons(types.JOIN,a,b)
        else:
            return helper.cons(types.JOIN,a,None)

    def getDictItems(self):
        a = self.getPrimary()
        col = self.match(types.COLON)    
        b = self.getPrimary()
        a.left = b
        if (self.check(types.COMMA)):
            self.advance()
            c = self.getDictItems()
            return helper.cons(types.JOIN,a,c)
        else:
            return helper.cons(types.JOIN,a,None)

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

    def getComparison(self):
        if(self.check(types.GREATERTHAN)):
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

    def getGate(self):
        if(self.check(types.OR)):
            return self.match(types.OR)
        elif(self.check(types.AND)):
            return self.match(types.AND)

    def opPending(self):
        return self.check(types.PLUS) or self.check(types.MINUS) or self.check(types.DIVIDE) or self.check(types.TIMES) or self.check(types.MOD) 

    def comparisonPending(self):
        return self.check(types.GREATERTHAN) or self.check(types.GREATERTHANEQUALTO) or self.check(types.LESSTHAN) or self.check(types.LESSTHANEQUALTO) or self.check(types.EQUALTO)  or self.check(types.NOTEQUAL) 

    def gatePending(self):
        return self.check(types.OR) or self.check(types.AND)


    def elsePending(self):
        return self.check(types.ELSE)

    def blockPending(self):
        return self.check(types.OBRACE)

    def dictItemsPending(self):
        return self.primaryPending()

    def varPending(self):
        return self.check(types.VAR)

    def statementPending(self):
        return self.ifStatementPending() or self.whileStatementPending() or self.functionDefPending() or self.idPending() or self.varPending()

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