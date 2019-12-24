# embed_mid

A quick project to be able to convert and play MIDI files on embedded devices.
It plays all the notes as square waves, ignoring the percussion channel.
It supports an arbitrary amount of simultaneous notes.
This should be trivial to include in your own projects. See `main.c` for usage.

It currently generates uint8 samples, this should be trivial to change.

## Requirements

* `player.c` and `player.h` has no dependencies.
* `convert.py` requires `mido` to read MIDI files:
  
  `pip3 install --user mido`


## Running it as is.

The player uses a simplified song format. You must convert your MIDI files first.

    ./convert.py MIDIFILE > songs.h && make [run/wav/mp3]

The reference implementation in `main.c` simply writes the audio samples to stdout.
Ensure `aplay` is installed to be able to hear the output if you `make run` it.

The Makefile also have the targets `wav` and `mp3` which will create a `out.filetype`.
These require `sox` and `lame` to be installed respectively.


## License

MIT, do whatever
