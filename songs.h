#include <stdint.h>
#include "player.h"

// {wait time in samples, channel index, target}
static const SongEvent my_song[] = {
	{0, 0, 50},
	{44100, 0, 100},
	{44100, 0, 50},
	{44100, 0, 30}
};
