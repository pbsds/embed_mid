#include <stdio.h>
#include "player.h"
#include "songs.h"

int main(void) {
	
	set_song(my_song);
	
	while (is_playing()){
		printf("%c", get_sample());
	}
	
	return 0;
}
