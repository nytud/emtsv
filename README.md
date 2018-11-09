# e-magyar-tsv

e-magyar text processing system -- new version

 * new architecture: inter-module communication system via tsv format
 * command line interface
 * REST API
 * implemented in Python

 __8 Nov 2018 MILESTONE#1__ =
morphological analysis + POS tagging
(emMorph + emLem + emTag) tested and works.
Also on a 1 million word chunk of text. :)

If a bug is found please leave feedback.

## Requirements

- Python 3.5 <=
- HFST 3.13 <=
- OpenJDK 8 =
- An UTF-8 locale must be set!

## Install

Clone together with submodules:

`git clone --recurse-submodules https://github.com/dlt-rilmta/e-magyar-tsv`

Cloning time is about 3 minutes.

`pip3 install Cython` (for emdeppy, must be installed in a separate step)

Then install requirements for submodules:

`pip3 install -r emmorphpy/requirements.txt`

`pip3 install -r purepospy/requirements.txt`

`pip3 install -r emdeppy/requirements.txt`

`pip3 install -r HunTag3/requirements.txt`

## Usage

__WARNING: The old API is deprecated and will be removed. Please consider testing emTSV20.py__

### Command-line interface

```
  echo "A kutya elment sétálni." > inputfile
  make RAWINPUT=inputfile test-morph-tag
```

That's it. :)

### REST API

Run the server of the desired program, or the pipeline. The commands are the following:

```bash
	# emMorph+emLem URL: http://127.0.0.1:5000/emMorph
	python3 ./emMorphREST.py
	# emTag URL: http://127.0.0.1:5000/emTag
	python3 ./emTagREST.py
	# DepTool URL: http://127.0.0.1:5000/emDepTool
	python3 ./depToolREST.py
	# emDep URL: http://127.0.0.1:5000/emDep
	python3 ./emDepREST.py
	# Chunker (XXX currently not working)
	python3 ./emChunkREST.py  URL: http://127.0.0.1:5000/emChunk
	# For the pipeline API 2.0 version (XXX beta):
	python3 ./emTSV20.py
```

The 2.0 API can be called with the URL scheme below where __command__ can be composed arbitrarily off the following modules separated by /:

- morph
- pos
- deptool
- chunk
- dep

__WARNING: The new API is still in Beta. Things may break without further notice!__

Example URLs:

- http://127.0.0.1:5000/morph
- http://127.0.0.1:5000/morph/pos
- http://127.0.0.1:5000/morph/pos/deptool/dep
- http://127.0.0.1:5000/deptool/dep

And the clients should call the server like below:

```python
	>>> import requests
	>>> r = requests.post('http://127.0.0.1:5000/command', files={'file':open('test.text', encoding='UTF-8')})
	>>> print(r.text)
	...
```

The format of __test.text__ file or stream must comply to the emTSV standards (header, column names, etc.) as for the CLI version. Please consult the examples for guidance!

### Python library

XXX Comming soon!

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
