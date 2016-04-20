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
	builtinFunctions = {"PRINTLN","LEN","PRINT","GET_INTEGER"}
	if(ide.getLexval().upper() in builtinFunctions):
		return lexer.lexeme(types.BUILTIN,ide.getLexval().upper())
	ids = env.left
	vals = env.right.left
	while (env != None):
		while (ids != None):
			if(ids.left == None):
				ids = ids.right
				vals = vals.right
			elif (ide.getLexval() == ids.left.getLexval()):
				return vals.left
			else:
				ids = ids.right
				vals = vals.right
			if (ids == None and env.right.right.left != None):                    # checking in outer scope
				env = env.right.right.left
				ids = env.left
				vals = env.right.left
		env = env.right.right.left   #outer env
	print("Error: Identifier",ide.getLexval() ,"not found")
	sys.exit()

def extendEnv(ids, vals, env):
	return cons(types.ENVIRONMENT,ids, cons(types.JOIN,vals,cons(types.JOIN, env,None)))

def assign(tree,env):
	return updateEnv(tree.left, eval(tree.right,env),env)

def evalDispatchAssign(tree,env):
	idname = tree.left
	obj = eval(idname,env)
	return updateEnv(tree.right.left, eval(tree.right.right,env),obj)

	# def evalDispatch(pt,env):
	# obj = eval(pt.right.left,env)
	# x = eval(pt.right.right,obj)
	# return x

def updateEnv(ide,val,env):
	ids = env.left
	vals = env.right.left
	while (env != None):
		while (ids != None):
			if(ids.left == None):
				ids = ids.right
				vals = vals.right
			elif (ide.getLexval() == ids.left.getLexval()):
				vals.left = val;
				return vals.left
			else:
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
	a = eval(pt.left,env)
	b = eval(pt.left.left,env)
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		#print(a.getLexval()+b.getLexval())
		return lexer.lexeme(types.INTEGER,a.getLexval()+b.getLexval())
	else:
		showerror("Error : Cannot add "+ a.getLextype()+ " with "+ b.getLextype())

def evalminus(pt,env):
	a = eval(pt.left,env)
	if(pt.left.left!=None):
		b = eval(pt.left.left,env)
		if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
			return lexer.lexeme(types.INTEGER,a.getLexval()-b.getLexval())
		else:
			showerror("Error : Cannot subtract "+ a.getLextype()+ " with "+ b.getLextype())
	else:
		if (a.getLextype() == "INTEGER"):
			return lexer.lexeme(types.INTEGER,-a.getLexval())
		else:
			showerror("Error: Should be a Integer")

def evaldivide(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.left.left,env)
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		if(b.getLexval()==0):
			showerror("Error: divide by zero")
		return lexer.lexeme(types.INTEGER,a.getLexval()/b.getLexval())
	else:
		showerror("Error : Cannot divide "+ a.getLextype()+ " with "+ b.getLextype())

def evaltimes(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.left.left,env)
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		return lexer.lexeme(types.INTEGER,a.getLexval()*b.getLexval())
	else:
		showerror("Error : Cannot multiply "+ a.getLextype()+ " with "+ b.getLextype())

def evalmod(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.left.left,env)
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		return lexer.lexeme(types.INTEGER,a.getLexval()%b.getLexval())
	else:
		showerror("Error : Cannot mod "+ a.getLextype()+ " with "+ b.getLextype())

def evalgreaterthan(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.right,env)
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		return lexer.lexeme(types.INTEGER,a.getLexval()>b.getLexval())
	else:
		showerror("Error : Cannot compare "+ a.getLextype()+ " with "+ b.getLextype())

def evalgreaterthanequalto(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.right,env)
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		return lexer.lexeme(types.INTEGER,a.getLexval()>=b.getLexval())
	else:
		showerror("Error : Cannot compare "+ a.getLextype()+ " with "+ b.getLextype())

def evallessthan(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.right,env)
	if (a.getLextype() == b.getLextype()):
		if(a.getLextype()=="INTEGER" or a.getLextype()=="STRING"):
			return lexer.lexeme(types.INTEGER,a.getLexval()<b.getLexval())
		else:
			showerror("Error : Cannot compare "+ a.getLextype()+ " with "+ b.getLextype())
	else:
		showerror("Error : Cannot compare "+ a.getLextype()+ " with "+ b.getLextype())

def evallessthanequalto(pt,env):
	a = eval(pt.left,env)
	b = eval(pt.right,env)
	if (a.getLextype() == b.getLextype()):
		if(a.getLextype()=="INTEGER" or a.getLextype()=="STRING"):
			return lexer.lexeme(types.INTEGER,a.getLexval()<=b.getLexval())
		else:
			showerror("Error : Cannot compare "+ a.getLextype()+ " with "+ b.getLextype())
	else:
		showerror("Error : Cannot compare "+ a.getLextype()+ " with "+ b.getLextype())

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
	if(a.getLextype() == "INTEGER" and a.getLexval()==True):
		return lexer.lexeme(types.INTEGER,a.getLexval())
	b = eval(pt.right,env)
	return lexer.lexeme(types.INTEGER,a.getLexval() or b.getLexval())

def evaland(pt,env):
	a = eval(pt.left,env)
	if(a.getLextype() == "INTEGER" and a.getLexval()==False):
		return lexer.lexeme(types.INTEGER,a.getLexval())
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

def stripParams(pt):
	if (pt.left == None):
		return pt
	elif(pt.left.getLextype()=="OPAREN"):
		a = pt.left.left
	elif(pt.left.getLextype()=="ID"):
		a = pt.left
	if (pt.right != None):
		b = stripParams(pt.right)
	else:
		b=None
	return cons(types.JOIN,a,b)

def evalfunctionDefination(pt,env):
	closure = lexer.lexeme(types.CLOSURE,None)
	closure.right = pt.right
	closure.left = env
	insert(pt.left,closure,env)

def evalfunctioncall(pt,env):
	arglist = pt.right.right
	functionName = pt.right.left
	closure = lookup(functionName,env)
	if(closure.getLextype()=="BUILTIN"):
		return evalBuiltin(closure,arglist,env)
	parameterlist = closure.right.left
	evaluatedArgs = evalargumentList(arglist,parameterlist,env)
	eparam = stripParams(parameterlist)
	definingEnv = closure.left
	newEnv = extendEnv(eparam,evaluatedArgs,definingEnv) #CHANGE TO env FOR DYNAMIC SCOPE
	functionbody = closure.right.right.left
	insert(lexer.lexeme(types.ID,"this"),newEnv,newEnv)
	return eval(functionbody,newEnv)

def evalBuiltin(builtinfunc,arglist,env):
	evaluatedArgs = evalargumentListforBuiltIn(arglist,env)
	name = builtinfunc.getLexval()
	if (name == "PRINTLN"):
		return evalPrintln(evaluatedArgs)
	if (name == "PRINT"):
		return evalPrint(evaluatedArgs)
	elif(name == "LEN"):
		return evalLen(evaluatedArgs)
	elif(name == "GET_INTEGER"):
		return evalGetInteger(evaluatedArgs)

def evalGetInteger(evaluatedArgs):
	return lexer.lexeme(types.INTEGER,int(evaluatedArgs.left.getLexval()))

def evalPrintln(evaluatedArgs):
	if(evaluatedArgs.left==None):
		print("\n")
	else:
		while(evaluatedArgs!=None):
			print(evaluatedArgs.left.getLexval(),end='')
			evaluatedArgs=evaluatedArgs.right
		print()

def evalPrint(evaluatedArgs):
	while(evaluatedArgs!=None):
		print(evaluatedArgs.left.getLexval(),end='')
		evaluatedArgs=evaluatedArgs.right

def evalLen(evaluatedArgs):
	if(evaluatedArgs.left.getLextype()=="ARRAY"):
		return lexer.lexeme(types.INTEGER,len(evaluatedArgs.left.getLexval()))
	else:
		showerror("Argument should be an array")

def evalargumentListforBuiltIn(pt,env):
	a = None
	if(pt.left!=None):
		a =eval(pt.left,env)
	if(pt.right!=None):
		b= evalargumentListforBuiltIn(pt.right,env)
	else:
		b=None
	return cons(types.JOIN,a,b)

def evalargumentList(args,params,env):
	if(args.left!=None and params.left!=None):
		if(params.left.getLextype()=="OPAREN"):
			a = lexer.lexeme(types.THUNK,None)
			a.left = args.left
			a.right = env
		else:
			a = eval(args.left,env)
	elif(args.left == None and params.left == None):
		a = None
		b = None
	if(args.left == None and params.left!= None):
		showerror("Error: Too few Arguments to the function..")
	elif(args.right != None and params.right== None):
		showerror("Error: Too many Arguments to the function..")
	elif(args.right != None and params.right!= None):
		b= evalargumentList(args.right,params.right,env)
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

def evalcollectionaccess(pt,env): #need to work on dictionary
	idname = pt.right.left
	expr = pt.right.right
	index = eval(expr,env)
	collection = lookup(idname,env)
	if(collection.getLextype()=="ARRAY"):
		if(index.getLextype()=="INTEGER"):
			if(index.getLexval()<len(collection.getLexval())):
				if(isinstance(collection.getLexval()[index.getLexval()],int)):
					return lexer.lexeme(types.INTEGER,collection.getLexval()[index.getLexval()])
				elif(isinstance(collection.getLexval()[index.getLexval()],str)):
					return lexer.lexeme(types.STRING,collection.getLexval()[index.getLexval()])
			else:
				showerror("index out of range..")
		else:
			showerror("index should be an Integer")

def evalcollectionupdate(pt,env):
	idname = pt.left
	index = eval(pt.right.left,env)
	newvalue = eval(pt.right.right.left,env)
	collection = lookup(idname,env)
	if(collection.getLextype()=="ARRAY"):
		if(index.getLextype()=="INTEGER"):
			if(index.getLexval()<len(collection.getLexval())):
				collection.getLexval()[index.getLexval()] = newvalue.getLexval()
			else:
				showerror("Index out of range")

def evalarrayappend(pt,env):
	idname = pt.left
	expr = pt.right
	collection = lookup(idname,env)
	if(collection.getLextype()=="ARRAY"):
		collection.getLexval().append(expr.getLexval())

def evallambdacall(pt,env):
	arglist = pt.right.left
	parameterlist = pt.right.right.left
	evaluatedArgs = evalargumentList(arglist,parameterlist,env)
	eparam = stripParams(parameterlist)
	newEnv = extendEnv(eparam,evaluatedArgs,env)
	body = pt.right.right.right.left
	return eval(body,newEnv)

def evallambda(pt,env):
	closure = lexer.lexeme(types.CLOSURE,None)
	closure.right = pt.right
	closure.left = env
	return closure

def evalDispatch(pt,env):
	obj = eval(pt.right.left,env)
	x = eval(pt.right.right,obj)
	return x

def eval(pt,env):
	if(pt == None):
		return
	if (pt.getLextype()== "INTEGER"):
		return pt
	elif (pt.getLextype()== "STRING"):
		return pt
	elif (pt.getLextype() == "ID"):
		x = lookup(pt,env)
		if (x.getLextype()=="THUNK"):
			y = eval(x,env)
			return y
		else: 
			return x
	elif (pt.getLextype()=="DISPATCH"):
		return evalDispatch(pt,env)
	elif (pt.getLextype()=="DISPATCHASSIGN"):
		evalDispatchAssign(pt,env)
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
		return evalarray(pt,env)
	elif (pt.getLextype() == "LAMBDACALL"):
		return evallambdacall(pt,env)		
	elif (pt.getLextype() == "LAMBDA"):
		return evallambda(pt,env)			
	elif (pt.getLextype() == "FUNCDEF"):
		evalfunctionDefination(pt,env)
	elif (pt.getLextype() == "FUNCTIONCALL"):
		return evalfunctioncall(pt,env)
	elif (pt.getLextype() == "ARGUMENTLIST"):
		return evalargumentList(pt,env)
	elif (pt.getLextype() == "IF"):
		return evalif(pt,env);
	elif (pt.getLextype() == "WHILE"):
		return evalwhileloop(pt,env)
	elif (pt.getLextype() == "COLLECTIONACCESS"):
		return evalcollectionaccess(pt,env);
	elif (pt.getLextype() == "COLLECTIONUPDATE"):
		return evalcollectionupdate(pt,env);
	elif (pt.getLextype() == "ARRAYAPPEND"):
		return evalarrayappend(pt,env)
	elif (pt.getLextype() == "THUNK"):
		return eval (pt.left,pt.right)
	elif (pt.getLextype()=="OPAREN"):
		return eval(pt.right,env)                     #expression added to right of oparen because in left the expresion chain is developed
	elif (pt.getLextype() == "STATEMENT"):
		returnval = eval(pt.left,env)
		if(pt.right!=None):
			pt = pt.right
			return eval(pt,env)
		else:
			return returnval


# def lookupENV(env):   #for testing
# 	print("Listing ENVIRONMENT...")
# 	ids = env.left
# 	vals = env.right.left
# 	#outerenv = env.right.right.left
# 	while (env != None):
# 		while (ids != None):
# 			if(vals.left != None and vals.left.getLextype()=="ARRAY"):
# 				print(ids.left.getLexval(), "= ",end="")
# 				print(vals.left.lex_val,sep=',')
# 			elif (vals.left != None and vals.left.getLextype()=="CLOSURE"):   #preety printing function
# 				print(ids.left.getLexval()+"(",end="")
# 				parameters = vals.left.right.left
# 				while(parameters!=None):
# 					if(parameters.right!=None):
# 						print(parameters.left.getLexval()+",",end="")
# 					else:
# 						print(parameters.left.getLexval()+")")
# 					parameters=parameters.right
# 				block = vals.left.right.right.left #need to print the intendlevel keep track of indentation level so if another block is enocunter tab is printed
# 				block.indent = block.indent+4
# 				print("{")
# 				preetyprint(block)
# 				print("}")

# 				block.indent = block.indent-4
# 			else:
# 				print (ids.left.getLexval(), "=", vals.left.getLexval())  #need to change if type changes like arrray
# 			ids = ids.right
# 			vals = vals.right
# 			if (ids == None and env.right.right.left != None):                    # checking in outer scope
# 				env = env.right.right.left
# 				ids = env.left
# 				vals = env.right.left
# 		env = env.right.right.left   #outer env
# 	print ("ENVIRONMENT ends...")



# def preetyprint(tree):
# 	if(tree == None):
# 		return
# 	elif(tree.getLextype()=="STATEMENT"):
# 		printindent(tree.indent)
# 		preetyprint(tree.left)
# 		print(";")
# 		preetyprint(tree.right)
# 	elif(tree.getLextype()=="TIMES"):
# 		preetyprint(tree.left)
# 		print("*",end='')
# 		preetyprint(tree.left.left)
# 	elif(tree.getLextype()=="ID"):
# 		print(tree.getLexval(),end='')

# def printindent(tempindent):
# 	#tempindent = indent;
# 	while(tempindent!=0):
# 		print(" ",end='')
# 		tempindent=tempindent-1









