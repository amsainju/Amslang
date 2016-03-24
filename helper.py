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
	print("Identifier not found")
	sys.exit()

def extendEnv(ids, vals, env):
	return cons(types.ENVIRONMENT,ids, cons(types.JOIN,vals,cons(types.JOIN, env,None)))

def assign(tree,env):
	return updateEnv(tree.left, eval(tree.right,env),env)   
	#print(newenv.right.left.getLextype())

def updateEnv(ide,val,env):
	#print("in update ",ide.getLextype(), ide.getLexval())
	lookupENV(env) #for testing
	a = cons(types.JOIN,ide,env.left)
	b = cons(types.JOIN,val,env.right.left)
	return cons(types.ENVIRONMENT,a,cons(types.JOIN,b,env.right.right))

def evalplus(pt,env):
	#print(pt.left.left.getLextype())
	a = eval(pt.left,env)
	b = eval(pt.left.left,env)
	#print(pt.left.getLextype())
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		#print(a.getLexval()+b.getLexval())
		return lexer.lexeme(types.INTEGER,a.getLexval()+b.getLexval())
	else:
		showerror("add not compatible")

def evalminus(pt,env):
	#print(pt.left.left.getLextype())
	a = eval(pt.left,env)
	b = eval(pt.left.left,env)
	#print(pt.left.getLextype())
	if (a.getLextype() == "INTEGER" and b.getLextype() == "INTEGER"):
		#print(a.getLexval()+b.getLexval())
		return lexer.lexeme(types.INTEGER,a.getLexval()-b.getLexval())
	else:
		showerror("minus not compatible")

def showerror(msg):
	print(msg)
	sys.exit()

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
		env = assign(pt,env)
		lookupENV(env)
	elif (pt.getLextype() == "STATEMENT"):
		eval(pt.left,env)
		pt = pt.right
		eval(pt,env)
	elif (pt.getLextype() == "PLUS"):
		return evalplus(pt,env)
	elif (pt.getLextype() == "MINUS"):
		return evalminus(pt,env)
	else:
		if (pt.right.getLextype() == "STATEMENT"):
			print("I should be here")
			return eval(pt.right.left,env)
		else:
			error("done")

def lookupENV(env):   #for testing
	print("Listing ENVIRONMENT...")
	ids = env.left
	vals = env.right.left
	#outerenv = env.right.right.left
	while (env != None):
		while (ids != None):
			print (ids.left.getLexval(), "=", vals.left.getLexval())
			ids = ids.right
			vals = vals.right
			if (ids == None and env.right.right.left != None):                    # checking in outer scope
				env = env.right.right.left
				ids = env.left
				vals = env.right.left
		env = env.right.right.left   #outer env
	print ("ENVIRONMENT ends...")








