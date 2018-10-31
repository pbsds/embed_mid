#!/usr/bin/env python3
import mido, sys
from collections import namedtuple


SongEvent = namedtuple("NameTuple", "t, channel, target")
# target is half of SAMPLERATE/note freq

SAMPLERATE = 44100

def note2freq(n):
	return 440*2**((n-57)/12)
def note2target(n):
	return int(SAMPLERATE / ( note2freq(n) * 2 ) + 0.698)

def convert_mido_midi_to_song_events(mid):
	midi_state = { # midi_state_2_song_event_channel
		channel : {}
		for channel in range(16)
	}
	song_event_channel = set() # taken or not
	
	t = 0
	for msg in mid:
		if msg.time > 0:
			t += msg.time*SAMPLERATE
		if hasattr(msg, "channel") and msg.channel == 9:
			continue # drums
			
		if msg.type == "note_on" and msg.velocity:
			if msg.note in midi_state[msg.channel]:
				channel = midi_state[msg.channel][msg.note]
			else:
				channel = 0
				while channel in song_event_channel:
					channel += 1
				midi_state[msg.channel][msg.note] = channel
				song_event_channel.add(channel)
			
			yield SongEvent(int(t), channel, note2target(msg.note))
			t -= int(t)
		elif msg.type == "note_off" \
		  or msg.type == "note_on" and msg.velocity == 0:
			channel = midi_state[msg.channel][msg.note]
			del midi_state[msg.channel][msg.note]
			song_event_channel.remove(channel)
			yield SongEvent(int(t), channel, 0)
			t -= int(t)
		elif msg.type == "pitchwheel":
			#msg.channel
			#float(msg.pitch)/8192.
			pass


def filter_song_events(events):
	#yield from events
	#return
	out = []
	for event in events:
		if event.t == 0:
			if out and out[-1].channel == event.channel:
				out[-1] = SongEvent(out[-1].t, event.channel, event.target)
			else:
				out.append(event)
		else:
			yield from out
			out.clear()
			out.append(event)
	yield from out


def song_events_to_c(events, name):
	events = list(events)
	return "\n".join([
		"#include <stdint.h>",
		"#include \"player.h\"",
		f"// Requires minimum {max(map(SongEvent.channel.fget, events))+1} channels",
		"",
		"// {wait time in samples, channel index, target}",

		f"static const SongEvent {name}[] = {{",
		*(f"\t{{{t:>7}, {channel:>3}, {target:>4}}},"
			for t, channel, target in events),
		"\t{0, 999999, 0} // end of song",
		"};",
	])

mid = mido.MidiFile(sys.argv[1])

events = convert_mido_midi_to_song_events(mid)
events = filter_song_events(events)
print(song_events_to_c(events, "my_song"))
