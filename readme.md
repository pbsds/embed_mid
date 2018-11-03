# embed_mid

A quick project to be able to convert and play MIDI files on embedded devices.
It plays all the notes as square waves, ignoring the percussion channel.
This should be trivial to include in your own projects. See `main.c` for usage.

It currently generates uint8 samples, this should be trivial to change.

## Requirements

* `player.c` and `player.h` has no dependencies.
* `convert.py` requires `remo` to read MIDI files:
  
  `pip3 install --user remo`


## Running it as is.

The player uses a simplified song format. You must convert your MIDI files first.

    ./convert.py MIDIFILE > songs.h && make [run]

The reference implementation in `main.c` simply writes the audio samples to stdout.
Ensure `aplay` is installed to be able to hear the output if you `run` it.


## Lisence

MIT, do whatever with it.
