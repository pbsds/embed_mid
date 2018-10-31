#include <stdint.h>
#include "player.h"

// {wait time in samples, channel index, target}
static const SongEvent* current_song;
static uint16_t current_state[CHANNELS][3] = {}; // [channel index] = {current_sample, counter, target}
static uint16_t current_sample = 0;
static uint32_t current_sample_counter = 0;
static uint16_t current_pos = 0;

void set_song(const SongEvent song[]) {
	current_sample = 0;
	current_sample_counter = 0;
	current_pos = 0;
	current_song = song;
}

uint8_t get_sample() {
	// step
	current_sample_counter++;
	while (current_sample_counter >= current_song[current_pos].time) {
		current_sample_counter = 0;
		
		uint16_t channel = current_song[current_pos].channel;
		uint16_t target = current_song[current_pos].target;
		if (channel > CHANNELS)
			return 0; // TODO: make something smarter
		current_state[channel][2] = target;
		if (!target) {
			current_sample -= current_state[channel][0];
			current_state[channel][1] = 0;
			current_state[channel][0] = 0;
		}
		
		current_pos++;
	}
	
	for (int i = 0; i < CHANNELS; i++) {
		if (current_state[i][2]){
			current_state[i][1]++;
			
			if (current_state[i][1] >= current_state[i][2]) {
				current_state[i][1] = 0;
				if (current_state[i][0]) {
					current_sample -= CHANNEL_AMPLITUDE;
					current_state[i][0] = 0;
				} else {
					current_sample += CHANNEL_AMPLITUDE;
					current_state[i][0] = CHANNEL_AMPLITUDE;
				}
			}
		}
	}
		
	
	return current_sample;
}
