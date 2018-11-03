
build: 
	gcc *.c -Ofast -o program -Werror=overflow

.PHONY : run
run: build
	./program | aplay -r 44100

.PHONY : clean
clean: 
	rm program

