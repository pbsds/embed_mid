#include <stdint.h>
#include "player.h"

// {wait time in samples, channel index, velocity, target}
static const SongEvent my_song[] = {
	{    0, 0, 16, 250},
	{44100, 0, 16, 500},
	{44100, 0, 16, 250},
	{44100, 0, 16, 150},
	{44100, 0, 16, 350},
	{0, -1, 0, 0}// channel index > CHANNELS means stop
};
