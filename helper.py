import lexeme
from type import types
def cons(ltype,leftlexeme,rightlexeme):
    intermediate = lexer.lexeme(ltype,None)
    intermediate.left = leftlexeme
    intermediate.right = rightlexeme
    return intermediate

def createEnv():
	return cons(tpyes.ENVIRONMENT,None, cons(types.JOIN,None,None))

def insert(id,val,env):
	ids = env.left
	values = env.right.left
	env.left = cons(types.JOIN,id,ids)
	env.right.left = cons(types.JOIN,val,values)



