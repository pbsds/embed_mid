#ifndef player_h_guard
#define player_h_guard


#include <stdint.h>

// {wait time in samples, channel index, target}
typedef struct {
	uint32_t time;
	uint16_t channel;
	uint16_t target;
} SongEvent;

#define SAMPLERATE 44100
#define CHANNELS 16

#define CHANNEL_AMPLITUDE 8

void set_song(const SongEvent song[]);
uint8_t get_sample();


#endif /* end of include guard: player_h_guard */
