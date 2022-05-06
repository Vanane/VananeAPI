# output file names
yaccOutput=yacc.out.c
yaccHOutput=yacc.out.h
lexOutput=lex.out.c


all: diceParser clean

diceParser: yacc.o
	cd ../ && mkdir -p bin
	cp yacc.o ../bin/diceParser


yacc.o: lex yacc stack.o tree.o JSONPrinter.o
	gcc -o yacc.o $(lexOutput) $(yaccOutput) stack.o tree.o JSONPrinter.o


lex:
	lex -o $(lexOutput) dice.l


yacc:
	yacc -o $(yaccOutput) -d dice.y


JSONPrinter.o: tree.o JSONPrinter.c
	gcc -o JSONPrinter.o -c JSONPrinter.c


clean:
	rm -rf *.o
	rm $(lexOutput)
	rm $(yaccOutput)
	rm $(yaccHOutput)
	