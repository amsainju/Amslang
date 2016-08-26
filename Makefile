default: 
	./ams test1.ams

run: 
	./ams test1.ams
	./ams test2.ams
	./ams test3.ams
	./ams test4.ams

cat-error1:
	cat error1.ams

run-error1:
	./ams error1.ams

cat-error2:
	cat error2.ams

run-error2:
	./ams error2.ams

cat-error3:
	cat error3.ams

run-error3:
	./ams error3.ams

cat-arrays:
	cat arrays.ams

run-arrays:
	./ams arrays.ams

cat-conditionals:
	cat conditionals.ams

run-conditionals:
	./ams conditionals.ams

cat-recursion:
	cat recursion.ams

run-recursion:
	./ams recursion.ams

cat-iteration:
	cat iteration.ams

run-iteration:
	./ams iteration.ams

cat-functions:
	cat functions.ams

run-functions:
	./ams functions.ams

cat-dictionary:
	cat dictionary.ams

run-dictionary:
	./ams dictionary.ams

cat-adder:
	cat adder.ams

run-adder:
	./ams adder.ams

clean:
	rm  -rf __pycache__/


cat-delayevaluation:
	cat delayevaluation.ams

run-delayevaluation:
	./ams delayevaluation.ams


