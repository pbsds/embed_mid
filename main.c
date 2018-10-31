#include <stdio.h>
#include "player.h"
#include "songs.h"

int main(void) {
	
	set_song(my_song);
	
	uint8_t s;
	while (1){
		s = get_sample();
		printf("%c", s);
	}
	
	return 0;
}
