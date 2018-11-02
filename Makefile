
build: 
	gcc *.c -Ofast -o program

.PHONY : run
run: build
	./program | aplay -r 44100

.PHONY : clean
clean: 
	rm program

