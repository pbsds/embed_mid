#include <stdio.h>
#include "player.h"
#include "songs.h"

int main(void) {
	
	set_song(my_song);
	
	while (1){
		printf("%c", get_sample());
	}
	
	return 0;
}
