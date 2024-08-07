#ifndef player_h_guard
#define player_h_guard


#include <stdint.h>
#include <stdbool.h>

// {wait time in samples, channel index, velocity, target}
typedef struct {
	uint32_t time;
	uint16_t channel; // this type might need to be expanded pending on requirements
	uint8_t velocity;
	uint16_t target; // n samples per half wavelength times TARGETSTEPS_PER_SAMPLE
} SongEvent;

#define SAMPLERATE 44100
#define TARGETSTEPS_PER_SAMPLE 5
#define CHANNELS 32
#define LOOP_SONG false /* do NOT enable this when making a wav/mp3! */

void set_song(const SongEvent song[]);
bool is_playing();
uint8_t get_sample();


#endif /* end of include guard: player_h_guard */
