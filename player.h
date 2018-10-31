#ifndef player_h_guard
#define player_h_guard


#include <stdint.h>

// {wait time in samples, channel index, velocity, target}
typedef struct {
	uint32_t time;
	uint8_t channel; // this type might need to be expanded pending on requirements
	uint8_t velocity;
	uint16_t target;
} SongEvent;

#define SAMPLERATE 44100
#define CHANNELS 32

void set_song(const SongEvent song[]);
uint8_t get_sample();


#endif /* end of include guard: player_h_guard */
