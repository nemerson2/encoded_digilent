# encoded_digilent
This package includes code for reading positional encoders using an Arduino, reading the scope off of an Analog Discovery 3 from Digilent, syncing the two sources of data, and saving into an excel. It was created originally for taking ultrasound measurements but could easily be applied to other sensor types.

double_enc_read.ino is the Aruino script needed for reading encoders

test_scope-wavegen.py uses the waveforms SDK (WF_SDK) to read the scope of the discovery 3. For testing purposes, code is included to also run the waveform generator.
