
build:
	gcc *.c -Ofast -o program -Werror=overflow

.PHONY : run
run: build
	./program | aplay -r 44100

.PHONY : wav
wav: build
	./program | sox -t raw -r 44100 -e unsigned -b 8 -c 1 - -r 44100 out.wav

.PHONY : mp3
mp3: build
	./program | lame -r -s 44.1 --bitwidth 8 --unsigned -m mono - out.mp3

.PHONY : clean
clean: 
	rm -f program out.wav out.mp3

