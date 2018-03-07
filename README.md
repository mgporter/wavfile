# wavfile
## What is it?
Wavfile is a lightweight wrapper for wav files.

## What can it do?
* Can import a wav file, providing a way to access information about the file such as number of channels, bitrate etc..
* Support for 16 bit files and 32 bit floating point files
* Presents wav data as a NumPy array within the `data` property
* Has a `plot()` method to plot wav data using pyplot
* Can write from NumPy array to a new wav file

## Usage
### Invoke:
`wavobject = Wav("path/to/wavfile.wav")`
### Plot:
`wavobject.plot()`
note: optional kwargs `xmin` and `xmax` define the part of the wav file you would like to look at, in samples
### Write:
`wavobject.write("path/to/new_wavfile.wav")`

## Things to add:
* Ways to transform the wav file
* Frequency analysis
* Simple volume controls such as normalization, compression, and expansion
* Combine multiple wav files
* Support for 24 bit files

## Things to improve:
* Efficiency of data import
