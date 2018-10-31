#include <stdint.h>

// {wait time in sample, channel index, wave}
typedef uint32_t SongEvent[3];

#define SAMPLERATE 44100
#define CHANNELS 16

#define AMPLITUDE_CHANNEL_MAX 50
#define AMPLITUDE_CHANNEL_MIN 0

void set_song(const SongEvent song[]);
uint8_t get_sample();
