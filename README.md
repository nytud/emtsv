# emTSV

TSV style format and REST API for e-magyar implemented in Python

 __8 Nov 2018 MILESTONE#1__ =
morphological analysis + POS tagging
(emMorph + emLem + emTag) tested and works.
Also on a 1 million word chunk of text. :)

This is a quick and dirty RFC implementation. Bugs can happen!
Please leave feedback!

## Requirements

python 3.5 <=

## Install

Clone together with submodules:

`git clone --recurse-submodules https://github.com/dlazesz/emTSV`

Cloning time is about 3 minutes.

`pip3 install Cython` (for emdeppy, must be installed in a separate step)

Then install requirements for submodules:

`pip3 install -r emmorphpy/requirements.txt`

`pip3 install -r purepospy/requirements.txt`

`pip3 install -r emdeppy/requirements.txt`

`pip3 install -r HunTag3/requirements.txt`

## Usage

### command line interface

```
  echo "A kutya elment sétálni." > inputfile
  make RAWINPUT=inputfile test-morph-tag > out
```

That's it. :)

### server

XXX TODO. This is just an old example for reference.

```
  python
	>>> import requests
	>>> r = requests.post('http://127.0.0.1:5000/command', files={'file':open('test.text', encoding='UTF-8')})
	>>> print(r.text)
	...
```

## Testing

```
time make test-morph > out.input.morph
time make test-morph-tag > out.input.morph-tag
time make test-tokenizedinput-morph-tag > out.input.morph-tag_alt
tkdiff out.input.morph out.input.morph-tag
diff out.input.morph-tag out.input.morph-tag_alt
```

The first diff shows the result of POS tagging.
<br/>
The second diff outputs nothing = the two files are the same.


There are some larger pre-tokenized testfiles available locally,
see `Makefile`.
<br/>
This command processes a 100 thousand words chunk of text,
works only on juniper and can take about 2 minutes:

```
time make TOKENIZEDINPUT=/store/projects/e-magyar/test_input/mnsz2_radio_100e.tok.test test-tokenizedinput-morph-tag > out.100e.tokenizedinput-morph-tag
```

To investigate the results:

```
view out.100e.tokenizedinput-morph-tag
```

An even larger text (1 million words) can be processed smoothly,
this works also only on juniper and can take about 20 (!) minutes:

```
time make TOKENIZEDINPUT=/store/projects/e-magyar/test_input/mnsz2_radio_1mio.tok.test test-tokenizedinput-morph-tag > out.1mio.tokenizedinput-morph-tag
```

```
view out.1mio.tokenizedinput-morph-tag
```

To test the guesser, type:

```
make RAWINPUT=test_input/halandzsa.test test-morph-tag > out.halandzsa.morph-tag
view out.halandzsa.morph-tag
```

The guesser also seems to work. :)
