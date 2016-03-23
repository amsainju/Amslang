import lexeme
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

def lookup(id,env):
	ids = env.left
	vals = env.right.left
	while (ids != None):
		if (id.getLexval() == ids.left.getLexval()):
			return vals.left
		ids = ids.right
		vals = vals.right
		if (ids == None and env.right.right.left != None):                    # checking in outer scope
			env = env.right.right.left
			ids = env.left
			vals = env.right.left
	print("Identifier not found")
	sys.exit()

def extendEnv(ids, vals, env):
	return cons(types.ENVIRONMENT,ids, cons(types.JOIN,vals,cons(types.JOIN, env,None)))







