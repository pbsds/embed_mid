#!/usr/bin/env python3
import mido, sys
from collections import namedtuple, defaultdict
from functools import partial
err = partial(print, file=sys.stderr)


SongEvent = namedtuple("NameTuple", "t, channel, velocity, target")
# target is half of the wavelength times TARGETSTEPS_PER_SAMPLE
# the player flips the square wave after overflowing the target

SAMPLERATE = 44100
TARGETSTEPS_PER_SAMPLE = 5
VELOCITY_SCALE = 8
LOWER_HIGHS = True
#LOWER_HIGHS = False # comment out this

def note2freq(n):
	return 440*2**((n-57)/12)
def note2target(n):
	return int(SAMPLERATE / ( note2freq(n) * 2 ) * TARGETSTEPS_PER_SAMPLE + 0.698)

def convert_mido_midi_to_song_events(mid):
	midi_state = {
		channel : {}
		for channel in range(16)
	}
	song_event_channel = set() # taken or not
	midi_channel_pitchwheels = [0]*16
	midi_channel_volume = [1.0]*16
	
	t = 0
	update_channel = False
	for msg in mid:
		if msg.time > 0:
			t += msg.time*SAMPLERATE
		if hasattr(msg, "channel") and msg.channel == 9:
			continue # drums
			
		if msg.type == "note_on" and msg.velocity:
			if msg.note in midi_state[msg.channel]:
				channel, _ = midi_state[msg.channel][msg.note]
			else:
				channel = 0
				while channel in song_event_channel:
					channel += 1
				song_event_channel.add(channel)

			velocity = msg.velocity * VELOCITY_SCALE / 128
			if LOWER_HIGHS:
				velocity *= (64-msg.note)/64 * 0.2  + 1

			midi_state[msg.channel][msg.note] = channel, velocity
			
			pitch = midi_channel_pitchwheels[msg.channel]
			volume = midi_channel_volume[msg.channel]
			yield SongEvent(int(t), channel, volume*velocity, note2target(msg.note+pitch))
			t -= int(t)
		elif msg.type == "note_off" \
		  or msg.type == "note_on" and msg.velocity == 0:
			try:
				channel, velocity = midi_state[msg.channel][msg.note]
			except KeyError:
				continue
			del midi_state[msg.channel][msg.note]
			song_event_channel.remove(channel)
			yield SongEvent(int(t), channel, velocity, 0)
			t -= int(t)
		elif msg.type == "control_change":
			if msg.control == 7:# channel colume
				midi_channel_volume[msg.channel] = msg.value / 127
				update_channel = True
		elif msg.type == "pitchwheel":
			pitch = msg.pitch / (8192/2)
			midi_channel_pitchwheels[msg.channel] = pitch
			update_channel = True
			
		if update_channel:
			update_channel = False
			pitch = midi_channel_pitchwheels[msg.channel]
			volume = midi_channel_volume[msg.channel]
			for note, (channel, velocity) in midi_state[msg.channel].items():
				yield SongEvent(int(t), channel, volume*velocity, note2target(note+pitch))
				t -= int(t)
			

def filter_overlapping_song_events(events):
	out = []
	for event in events:
		if event.t == 0:
			if out and out[-1].channel == event.channel:
				out[-1] = SongEvent(out[-1].t, event.channel, event.velocity, event.target)
			else:
				out.append(event)
		else:
			yield from out
			out.clear()
			out.append(event)
	yield from out

def filter_redundant_song_events(events):
	channels = defaultdict(lambda: [0, 0])# channel : [target, velocity]
	out = []
	t = 0
	for event in events:
		this = [int(event.target), int(event.velocity+0.5)]
		if channels[event.channel] == this:
			t += event.t # filter this event, but keeping time
		else:
			if t:
				yield SongEvent(event.t+t, *event[1:])
				t = 0
			else:
				yield event
		channels[event.channel] = this
	yield from out

def song_events_to_c(events, name):
	events = list(events)
	nchannels = max(map(SongEvent.channel.fget, events))+1
	err(f"This song requires minimum {nchannels} channels")
	err(f"If you get a -Werror=overflow error, then change the type of SongEvent.channel in player.h")
	err()
	return "\n".join([
		"#include <stdint.h>",
		"#include \"player.h\"",
		"",
		f"#if (CHANNELS < {nchannels})",
		f"#error \"Not enough CHANNELS, defined in player.h. Minimum {nchannels} required!\"",
		"#endif",
		"",
		"// {wait time in samples, channel index, velocity, target}",
		
		f"static const SongEvent {name}[] = {{",
		*(f"\t{{{t:>7}, {channel:>3}, {int(velocity+0.5):>3}, {target:>4}}},"
			for t, channel, velocity, target in events),
		"\t{0, -1, 0, 0} // end of song",
		"};",
	])


if __name__ == "__main__":
	if not len(sys.argv) >= 2:
		print("Usage:")
		print(f"\t{sys.argv[0]} MIDIFILE > songs.h && make [run]")
		exit()
	
	mid = mido.MidiFile(sys.argv[1])
	
	events = convert_mido_midi_to_song_events(mid)
	events = filter_overlapping_song_events(events)
	events = filter_redundant_song_events(events)
	print(song_events_to_c(events, "my_song"))
