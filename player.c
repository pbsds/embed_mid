#include <stdint.h>
#include "player.h"

static const SongEvent* current_song;
static uint16_t current_sample = 0;

void set_song(const SongEvent song[]) {
	current_sample = 0;
}

uint8_t get_sample() {
	if (current_sample == AMPLITUDE_CHANNEL_MAX){
		current_sample = AMPLITUDE_CHANNEL_MIN;
	} else {
		current_sample = AMPLITUDE_CHANNEL_MAX;
	}
	
	return current_sample;
}
