default: 
	./recognizer test1.txt

run: 
	./recognizer test1.txt
	./recognizer test2.txt
	./recognizer test3.txt
	./recognizer test4.txt

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


