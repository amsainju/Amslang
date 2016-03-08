#Author: Arpan Man Sainju
#Date: 02/17/2016
#Description: contains two classes. Class lexer have lex module that read a character from a file at a time and returns the lexemes. 
#             Class lexeme stores the type of the token and/or value associated with the token. 
from type import types
class lexer:
    lineNumber = 1
    
    def __init__(self,source):
        self.sfile = open(source)
    
    def getCharacter(self):
        return self.sfile.read(1)
    
    def updateLineNumber(self,ch):
        if(ch == "\n"):
            lexer.lineNumber = lexer.lineNumber + 1   
            
    def skipwhitespaces(self):
        ch = self.getCharacter()
        if (ch == '\n'):
            lexer.lineNumber = lexer.lineNumber + 1
            self.skipwhitespaces()
        else:
            while (ch== " " or ch=="#" or  ch == "\t" or ch == "\n"):
                if(ch == "#"):                                     
                    ch = self.getCharacter()
                    self.updateLineNumber(ch) 
                    if (ch =="#"):                           #deals with multi-block comment
                        notok =True
                        while(notok):
                            ch = self.getCharacter()
                            self.updateLineNumber(ch) 
                            if ch == "#":
                                ch2 = self.getCharacter()
                                self.updateLineNumber(ch) 
                                if ch2 == "#":
                                    ch = self.getCharacter()
                                    self.updateLineNumber(ch) 
                                    notok = False 
                    else:       
                        while(ch != "\n"):                  #deals with single line comment
                            ch = self.getCharacter()
                        lexer.lineNumber = lexer.lineNumber + 1
                else:
                    ch = self.getCharacter()
                    self.updateLineNumber(ch) 
            self.pushbackOneCharacter(ch)
               
    def pushbackOneCharacter(self,ch):
        if ch:
            self.sfile.seek(self.sfile.tell()-1) #it ch is not end of file pushback
        
    def getLexeme(self,ch):
        #SIGNLE CHARACTER TOKENS
        if(ch == "\n"):
            return lexeme(types.NEWLINE,None);
        if(ch == ""):
            return lexeme(types.END_OF_FILE,None);
        if(ch == '('):
            return lexeme(types.OPAREN,None);
        if(ch == ')'):
            return lexeme(types.CPAREN,None);
        if(ch == '{'):
            return lexeme(types.OBRACE,None);
        if(ch == '}'):
            return lexeme(types.CBRACE,None);
        if(ch == '['):
            return lexeme(types.OSQBRACE,None);
        if(ch == ']'):
            return lexeme(types.CSQBRACE,None);
        if(ch == ','):
            return lexeme(types.COMMA,None);
        if(ch == '+'):
            return lexeme(types.PLUS,None);
        if(ch == '-'):
            return lexeme(types.MINUS,None);
        if(ch == '/'):
            return lexeme(types.DIVIDE,None);
        if(ch == '*'):
            return lexeme(types.TIMES,None);
        if(ch == '%'):
            return lexeme(types.MOD,None);
        if(ch == ':'):
            return lexeme(types.COLON,None);
        if(ch == '.'):
            return lexeme(types.DOT,None);
        if(ch == ';'):
            return lexeme(types.SEMI,None);
        #END SINGLE CHARACTER TOKEN
        
        #MULTI CHARACTER TOKENS START
        if(ch == '"'):
            return self.lexString();
        if(ch == '='):
            ch2 = self.getCharacter()
            if(ch2 == '='):
                return lexeme(types.EQUALTO,None)
            else:
                self.pushbackOneCharacter(ch2)
                return lexeme(types.ASSIGN,None);
        if(ch == '>'):
            ch2 = self.getCharacter()
            if(ch2 == '='):
                return lexeme(types.GREATERTHANEQUALTO,None)
            else:
                self.pushbackOneCharacter(ch2)
                return lexeme(types.GREATERTHAN,None);
        if(ch == '<'):
            ch2 = self.getCharacter()
            if(ch2 == '='):
                return lexeme(types.LESSTHANEQUALTO,None)
            else:
                self.pushbackOneCharacter(ch2)
                return lexeme(types.LESSTHAN,None);
        if(ch == '!'):
            ch2 = self.getCharacter()
            if(ch2 == '='):
                return lexeme(types.NOTEQUAL,None)
            else:
                self.pushbackOneCharacter(ch2)
                return lexeme(types.BADCHARACTER,None);    
 
        if(ch.isalpha()):
            return self.lexWord(ch)
        if(ch.isdigit()):
            return self.lexNumber(ch)
        else:
            #print("ch=",ch)
            return lexeme(types.BADCHARACTER,ch)       
                                                    
                                                   
    
    def lexNumber(self,ch):
        buffer = ""
        numbers ={'0','1','2','3','4','5','6','7','8','9'}
        while(ch in numbers):
            buffer += ch
            ch = self.getCharacter()
        self.pushbackOneCharacter(ch)
        return lexeme(types.INTEGER,int(buffer))
    
    def lexWord(self,ch):
        buffer = ""
        notvalidcharacters = {"",'\t','\n',' ',';',',','(',')','%','[',']','{','}','.','-','+','*','&','^','\\','<','>','?','=','|','#','~','`',':','!','@','&'}
        keywords = {'define','lambda','print','else','if','while','input','and','or'}
        while(ch not in notvalidcharacters):
            buffer += ch
            ch = self.getCharacter()
        self.pushbackOneCharacter(ch)  
        if (buffer in keywords):
            #print("buffer =",buffer.upper())
            if (buffer.upper() == "DEFINE"):
                return lexeme(types.DEFINE,None)
            elif (buffer.upper() == "LAMBDA"):
                return lexeme(types.LAMBDA,None)
            elif (buffer.upper() == "PRINT"):
                return lexeme(types.PRINT,None)
            elif (buffer.upper() == "ELSE"):
                return lexeme(types.ELSE,None)
            elif (buffer.upper() == "IF"):
                return lexeme(types.IF,None)
            elif (buffer.upper() == "WHILE"):
                return lexeme(types.WHILE,None)
            elif (buffer.upper() == "OR"):
                return lexeme(types.OR,None)  
            elif (buffer.upper() == "INPUT"):
                return lexeme(types.INPUT,None)
            elif (buffer.upper() == "AND"):
                return lexeme(types.AND,None)
            else:
                return lexeme(types.BADCHARACTER,buffer)         
        else:
            return lexeme(types.ID,buffer)
        
    def lexString(self):
        buffer = ""
        ch = self.getCharacter()
        while(ch != '"'):
            if(ch == "\\"):
                ch= self.getCharacter()
            buffer+= ch
            ch = self.getCharacter()
        return lexeme(types.STRING,buffer)
    
    def lex(self):
        self.skipwhitespaces()
        ch = self.getCharacter()
        return self.getLexeme(ch)
    

class lexeme:   
    def __init__(self,lex_type,lex_val):
        self.lex_type = lex_type
        self.lex_val = lex_val
        self.left = None
        self.right = None
        
    def setleft(self,left):
        self.left = left

    def setright(self,right):
        self.right = right
        
    def getLextype(self):
        return self.lex_type
    
    def getLexval(self):
        return self.lex_val

    def getleft(self):
        return self.left
    
    def getright(self):
        return self.right