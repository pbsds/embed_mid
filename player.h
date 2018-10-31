#include <stdint.h>

// {wait time in samples, channel index, target}
typedef uint32_t SongEvent[3];

#define SAMPLERATE 44100
#define CHANNELS 16

#define CHANNEL_AMPLITUDE 8

void set_song(const SongEvent song[]);
uint8_t get_sample();
