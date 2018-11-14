#include <stdint.h>
#include <stdbool.h>
#include "player.h"

struct State {
	uint16_t current_sample;
	uint16_t counter;
	uint16_t target;
	uint8_t velocity;
};

// {wait time in samples, channel index, velocity, target}
static const SongEvent* current_song;
static struct State current_state[CHANNELS] = {};
static uint16_t current_sample = 0;
static uint32_t current_sample_counter = 0;
static uint32_t current_pos = 0;
static bool current_playing = false;

void set_song(const SongEvent song[]) {
	current_sample = 0;
	current_sample_counter = 0;
	current_pos = 0;
	current_playing = true;
	current_song = song;
}

bool is_playing() {
	return current_playing;
}

uint8_t get_sample() {
	// step
	current_sample_counter++;
	while (current_sample_counter >= current_song[current_pos].time) {
		current_sample_counter = 0;
		
		uint32_t channel = current_song[current_pos].channel;
		uint8_t velocity = current_song[current_pos].velocity;
		uint16_t target = current_song[current_pos].target;
		if (channel > CHANNELS) {
			if (LOOP_SONG) {
				current_pos = 0;
				continue;
			} else {
				current_playing = false;
				return 0;
			}
		}
		current_state[channel].target = target;
		current_state[channel].velocity = velocity;
		if (!target) {
			current_sample -= current_state[channel].current_sample;
			current_state[channel].counter = 0;
			current_state[channel].current_sample = 0;
		}
		
		current_pos++;
	}
	
	for (int i = 0; i < CHANNELS; i++) {
		if (current_state[i].target){
			current_state[i].counter += TARGETSTEPS_PER_SAMPLE;
		
			if (current_state[i].counter >= current_state[i].target) {
				current_state[i].counter -= current_state[i].target;
				if (current_state[i].current_sample) {
					current_sample -= current_state[i].current_sample;
					current_state[i].current_sample = 0;
				} else {
					current_sample += current_state[i].velocity;
					current_state[i].current_sample = current_state[i].velocity;
				}
			}
		}
	}
		
	
	return current_sample;
}
