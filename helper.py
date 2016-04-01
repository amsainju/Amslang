import lexer
import sys
from type import types


def cons(ltype,leftlexeme,rightlexeme):
    intermediate = lexer.lexeme(ltype,None)
    intermediate.left = leftlexeme
    intermediate.right = rightlexeme
    return intermediate

def createEnv():
	return extendEnv(None,None,None);

def insert(id,val,env):
	ids = env.left
	values = env.right.left
	env.left = cons(types.JOIN,id,ids)
	env.right.left = cons(types.JOIN,val,values)

def lookup(ide,env):
	builtinFunctions = {"SHOW","APPEND","LOAD"}
	if(ide.getLexval().upper() in builtinFunctions):
		return lexer.lexeme(types.BUILTIN,ide.getLexval().upper())
	ids = env.left
	vals = env.right.left
	#outerenv = env.right.right.left
	while (env != None):
		while (ids != None):
			if (ide.getLexval() == ids.left.getLexval()):
				return vals.left
			ids = ids.right
			vals = vals.right
			if (ids == None and env.right.right.left != None):                    # checking in outer scope
				env = env.right.right.left
				ids = env.left
				vals = env.right.left
		env = env.right.right.left   #outer env
	print("Identifier",ide.getLexval() ,"not found")
	sys.exit()

def extendEnv(ids, vals, env):
	return cons(types.ENVIRONMENT,ids, cons(types.JOIN,vals,cons(types.JOIN, env,None)))

def assign(tree,env):
	return updateEnv(tree.left, eval(tree.right,env),env)   
	#print(newenv.right.left.getLextype())

def updateEnv(ide,val,env):
	ids = env.left
	vals = env.right.left
	#outerenv = env.right.right.left
	while (env != None):
		while (ids != None):
			if (ide.getLexval() == ids.left.getLexval()):
				vals.left = val;
				return vals.left
			ids = ids.right
			vals = vals.right
			if (ids == None and env.right.right.left != None):                    # checking in outer scope
				env = env.right.right.left
				ids = env.left
				vals = env.right.left
		env = env.right.right.left   #outer env
	print("Identifier",ide.getLexval() ,"used without declaration.")
	sys.exit()

def evalplus(pt,env):
	#print(pt.left.left.getLextype())
	#print(pt.left.getLextype());
	a = eval(pt.left,env)
	b = eval(pt.left.left,env)
	#print(a.getLexval()," and ",b.getLexval())
	#print(pt.left.getLextype())
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		#print(a.getLexval()+b.getLexval())
		return lexer.lexeme(types.INTEGER,a.getLexval()+b.getLexval())
	else:
		showerror("+ not compatible")

def evalminus(pt,env):
	#print(pt.left.left.getLextype())
	a = eval(pt.left,env)
	if(pt.left.left!=None):
		b = eval(pt.left.left,env)
		#print(pt.left.getLextype())
		if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
			#print(a.getLexval()+b.getLexval())
			return lexer.lexeme(types.INTEGER,a.getLexval()-b.getLexval())
		else:
			showerror("- not compatible")
	else:
		if (a.getLextype() == "INTEGER"):
			return lexer.lexeme(types.INTEGER,-a.getLexval())
		else:
			showerror("Should be a Integer")

def evaldivide(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.left.left,env)
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		if(b.getLexval()==0):
			showerror("Error: divide by zero")
		return lexer.lexeme(types.INTEGER,a.getLexval()/b.getLexval())
	else:
		showerror("/ not compatible")

def evaltimes(pt,env):
	#print("evaltimes a = ",pt.left.getLextype(),pt.left.getLexval())
	#print("evaltimes b = ",pt.left.left.getLextype(),pt.left.left.getLexval())
	#lookupENV(env)
	a = eval(pt.left,env)
	b = eval(pt.left.left,env)
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		return lexer.lexeme(types.INTEGER,a.getLexval()*b.getLexval())
	else:
		showerror("* not compatible")

def evalmod(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.left.left,env)
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		return lexer.lexeme(types.INTEGER,a.getLexval()%b.getLexval())
	else:
		showerror("% not compatible")

def evalgreaterthan(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.right,env)
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		return lexer.lexeme(types.INTEGER,a.getLexval()>b.getLexval())
	else:
		showerror("> not compatible")

def evalgreaterthanequalto(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.right,env)
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		return lexer.lexeme(types.INTEGER,a.getLexval()>=b.getLexval())
	else:
		showerror(">= not compatible")

def evallessthan(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.right,env)
	if (a.getLextype() == b.getLextype()):
		if(a.getLextype()=="INTEGER" or a,getLextype()=="STRING"):
			return lexer.lexeme(types.INTEGER,a.getLexval()<b.getLexval())
		else:
			showerror(a.getLextype()+" and "+b.getLextype()+" not compatible for < comparision")
	else:
		showerror(a.getLextype()+" and "+b.getLextype()+" not compatible for < comparision")

def evallessthanequalto(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.right,env)
	if (a.getLextype() == b.getLextype()):
		if(a.getLextype()=="INTEGER" or a,getLextype()=="STRING"):
			return lexer.lexeme(types.INTEGER,a.getLexval()<=b.getLexval())
		else:
			showerror(a.getLextype()+" and "+b.getLextype()+" not compatible for <= comparision")
	else:
		showerror(a.getLextype()+" and "+b.getLextype()+" not compatible for <= comparision")

def evalequalto(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.right,env)
	return lexer.lexeme(types.INTEGER,a.getLexval()==b.getLexval())

def evalnotequalto(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.right,env)
	return lexer.lexeme(types.INTEGER,a.getLexval()!=b.getLexval())

def evalor(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.right,env)
	return lexer.lexeme(types.INTEGER,a.getLexval() or b.getLexval())

def evaland(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.right,env)
	return lexer.lexeme(types.INTEGER,a.getLexval() and b.getLexval())


def showerror(msg):
	print(msg)
	sys.exit()

def evalarray(pt,env):
	array = lexer.lexeme(types.ARRAY,[])
	next = pt.left
	while(next != None):
		item = eval(next.left,env);
		array.lex_val.append(item.getLexval())
		next = next.right
	return array


def evalfunctionDefination(pt,env):
	closure = lexer.lexeme(types.CLOSURE,None)
	closure.right = pt.right
	closure.left = env
	insert(pt.left,closure,env)

def evalfunctioncall(pt,env):
	arglist = pt.right.right
	evaluatedArgs = evalargumentList(arglist,env)
	functionName = pt.right.left
	closure = lookup(functionName,env)
	if(closure.getLextype()=="BUILTIN"):
		return evalBuiltin(closure,evaluatedArgs,env)
	parameterlist = closure.right.left
	definingEnv = closure.left
	newEnv = extendEnv(parameterlist,evaluatedArgs,definingEnv) #CHANGE TO env FOR DYNAMIC SCOPE
	functionbody = closure.right.right.left
	return eval(functionbody,newEnv)

def evalBuiltin(builtinfunc,evaluatedargs,env):
	name = builtinfunc.getLexval()
	if (name == "SHOW"):
		return evalShow(evaluatedargs)

def evalShow(evaluatedArgs):
	while(evaluatedArgs!=None):
		print(evaluatedArgs.left.getLexval(),end='')
		evaluatedArgs=evaluatedArgs.right
	print()

def evalargumentList(pt,env):
	if(pt.left!=None):
		a =eval(pt.left,env)
	if(pt.right!=None):
		b= eval(pt.right,env)
	else:
		b=None
	return cons(types.JOIN,a,b)

def evalif(pt,env):
	cond = eval(pt.left,env)
	if(cond.getLexval()==True):
		body = pt.right.left
		return eval(body,env)
	else:
		elsecase = pt.right.right
		if(elsecase!=None and elsecase.getLextype()=="ELSE"):
			return eval(elsecase.left,env)

def evalwhileloop(pt,env):
	cond = eval(pt.left,env)
	if(cond.getLexval()==True):
		body = pt.right
		eval(body,env)
		return evalwhileloop(pt,env)



def eval(pt,env):
	if(pt == None):
		return
	if (pt.getLextype()== "INTEGER"):
		return pt
	elif (pt.getLextype()== "STRING"):
		return pt
	elif (pt.getLextype() == "ID"):
		return lookup(pt,env)
	elif (pt.getLextype()== "ASSIGN"):
		assign(pt,env)
	elif (pt.getLextype() == "PLUS"):
		return evalplus(pt,env)
	elif (pt.getLextype() == "MINUS"):
		return evalminus(pt,env)
	elif (pt.getLextype() == "DIVIDE"):
		return evaldivide(pt,env)
	elif (pt.getLextype() == "TIMES"):
		return evaltimes(pt,env)
	elif (pt.getLextype() == "MOD"):
		return evalmod(pt,env)
	elif (pt.getLextype() == "GREATERTHAN"):
		return evalgreaterthan(pt,env)
	elif (pt.getLextype() == "GREATERTHANEQUALTO"):
		return evalgreaterthanequalto(pt,env)
	elif (pt.getLextype() == "LESSTHAN"):
		return evallessthan(pt,env)
	elif (pt.getLextype() == "LESSTHANEQUALTO"):
		return evallessthanequalto(pt,env)
	elif (pt.getLextype() == "EQUALTO"):
		return evalequalto(pt,env)
	elif (pt.getLextype() == "NOTEQUAL"):
		return evalnotequalto(pt,env)
	elif (pt.getLextype() == "OR"):
		return evalor(pt,env)
	elif (pt.getLextype() == "AND"):
		return evaland(pt,env)
	elif (pt.getLextype() == "VAR"):
		insert(pt.left,eval(pt.right,env),env)
	elif (pt.getLextype() == "ARRAY"):
		return evalarray(pt,env);
	elif (pt.getLextype() == "LAMBDA"):
		return 						#TODO
	elif (pt.getLextype() == "FUNCDEF"):
		evalfunctionDefination(pt,env);
	elif (pt.getLextype() == "FUNCTIONCALL"):
		return evalfunctioncall(pt,env);
	elif (pt.getLextype() == "ARGUMENTLIST"):
		return evalargumentList(pt,env);
	elif (pt.getLextype() == "IF"):
		return evalif(pt,env);
	elif (pt.getLextype() == "WHILE"):
		return evalwhileloop(pt,env);
	elif (pt.getLextype()=="OPAREN"):
		return eval(pt.right,env)                     #expression added to right of oparen because in left the expresion chain is developed
	elif (pt.getLextype() == "STATEMENT"):
		returnval = eval(pt.left,env)
		if(pt.right!=None):
			pt = pt.right
			return eval(pt,env)
		else:
			return returnval


def lookupENV(env):   #for testing
	print("Listing ENVIRONMENT...")
	ids = env.left
	vals = env.right.left
	#outerenv = env.right.right.left
	while (env != None):
		while (ids != None):
			if(vals.left != None and vals.left.getLextype()=="ARRAY"):
				print(ids.left.getLexval(), "= ",end="")
				print(vals.left.lex_val,sep=',')
			elif (vals.left != None and vals.left.getLextype()=="CLOSURE"):   #preety printing function
				print(ids.left.getLexval()+"(",end="")
				parameters = vals.left.right.left
				while(parameters!=None):
					if(parameters.right!=None):
						print(parameters.left.getLexval()+",",end="")
					else:
						print(parameters.left.getLexval()+")")
					parameters=parameters.right
				block = vals.left.right.right.left #need to print the intendlevel keep track of indentation level so if another block is enocunter tab is printed
				block.indent = block.indent+4
				print("{")
				preetyprint(block)
				print("}")

				block.indent = block.indent-4
			else:
				print (ids.left.getLexval(), "=", vals.left.getLexval())  #need to change if type changes like arrray
			ids = ids.right
			vals = vals.right
			if (ids == None and env.right.right.left != None):                    # checking in outer scope
				env = env.right.right.left
				ids = env.left
				vals = env.right.left
		env = env.right.right.left   #outer env
	print ("ENVIRONMENT ends...")



def preetyprint(tree):
	if(tree == None):
		return
	elif(tree.getLextype()=="STATEMENT"):
		printindent(tree.indent)
		preetyprint(tree.left)
		print(";")
		preetyprint(tree.right)
	elif(tree.getLextype()=="TIMES"):
		preetyprint(tree.left)
		print("*",end='')
		preetyprint(tree.left.left)
	elif(tree.getLextype()=="ID"):
		print(tree.getLexval(),end='')

def printindent(tempindent):
	#tempindent = indent;
	while(tempindent!=0):
		print(" ",end='')
		tempindent=tempindent-1









