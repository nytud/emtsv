
<!--
 - M#1-nek megfelelő README.md legyen =
maradjunk meg a production release-re (jelenleg ez a MILESTONE#1)
vonatkozó infók közlésénél,
minden, ami azon túl van, az legyen a
[Work in progress](#work-in-progress)
részben (jövőbeli MILESTONE-ok szerint).
-->

# e-magyar-tsv

__e-magyar__ text processing system -- new version

 * new architecture: inter-module communication via tsv format
 * easy to use command-line interface
 * convenient REST API
 * implemented in Python

 __8 Nov 2018 MILESTONE#1 (production)__ =
morphological analysis + POS tagging
(emMorph + emLem + emTag) tested and works.
Also on a 1 million word chunk of text. :)

If you use __e-magyar-tsv__,
please cite the following former articles
(while our new paper is in preparation):

    Váradi Tamás, Simon Eszter, Sass Bálint, Mittelholcz Iván, Novák Attila, Indig Balázs: E-magyar – A Digital Language Processing System. In: Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018), 1307-1312.

    Váradi Tamás, Simon Eszter, Sass Bálint, Gerőcs Mátyás, Mittelholcz Iván, Novák Attila, Indig Balázs, Prószéky Gábor, Farkas Richárd, Vincze Veronika: Az e-magyar digitális nyelvfeldolgozó rendszer. In: MSZNY 2017, XIII. Magyar Számítógépes Nyelvészeti Konferencia, Szeged: Szegedi Tudományegyetem Informatikai Tanszékcsoport, 49-60.

This system is a replacement for the original
https://github.com/dlt-rilmta/hunlp-GATE system.

If a bug is found please leave feedback.

## Requirements

- Python 3.5 <=
- HFST 3.13 <=
<br/>
On Ubuntu 18.04,
an `apt-get install hfst` is enough,
as HFST 3.13 is the default is this version.
- OpenJDK 8
<br/>
We encountered problems using OpenJDK 11 (#1),
so we recommend using OpenJDK 8.
- An UTF-8 locale must be set.

## Install

Clone together with submodules (it takes about 3 minutes):

`git clone --recurse-submodules https://github.com/dlt-rilmta/e-magyar-tsv`

Install `Cython` for `emdeppy`. It must be installed in a separate step.

`pip3 install Cython`

Then install requirements for submodules:

`pip3 install -r emmorphpy/requirements.txt`

`pip3 install -r purepospy/requirements.txt`

`pip3 install -r emdeppy/requirements.txt`

`pip3 install -r HunTag3/requirements.txt`

## Usage

_Remark:_ Now we use tsvAPI1.0.
This will be deprecated, removed and changed to tsvAPI2.0
(maybe at __MILESTONE#3__).

### Command-line interface

```bash
  echo "A kutya elment sétálni." > inputfile
  make RAWINPUT=inputfile test-morph-tag
```

That's it. :)

### REST API

To start the server of the desired module,
use (without the `--pipe` switch):

```bash
	# emMorph+emLem URL: http://127.0.0.1:5000/emMorph
	python3 ./emMorphREST.py
	# emTag URL: http://127.0.0.1:5000/emTag
	python3 ./emTagREST.py
	# DepTool URL: http://127.0.0.1:5000/emDepTool
	python3 ./depToolREST.py
	# emDep URL: http://127.0.0.1:5000/emDep
	python3 ./emDepREST.py
	# emChunk URL: http://127.0.0.1:5000/emChunk -- XXX currently not working
	python3 ./emChunkREST.py
```

To use the started servers the clients should call them like:

```python
	>>> import requests
	>>> r = requests.post('http://127.0.0.1:5000/command', files={'file':open('test.text', encoding='UTF-8')})
	>>> print(r.text)
	...
```

The format of `test.text` file or stream
must comply to the __e-magyar-tsv__ standards (header, column names, etc.)
as for the CLI version. Please consult the examples for guidance.
(XXX which examples?)

## Testing

_Remark:_ This testing uses tsvAPI1.0.
This will be deprecated, removed and changed to tsvAPI2.0
(maybe at __MILESTONE#3__).
In the meantime,
please consider testing emTSV20.py which is built with tsvAPI2.0.

```bash
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

```bash
time make TOKENIZEDINPUT=/store/projects/e-magyar/test_input/mnsz2_radio_100e.tok.test test-tokenizedinput-morph-tag > out.100e.tokenizedinput-morph-tag
```

To investigate the results:

```bash
view out.100e.tokenizedinput-morph-tag
```

An even larger text (1 million words) can be processed smoothly,
this works also only on juniper and can take about 20 (!) minutes:

```bash
time make TOKENIZEDINPUT=/store/projects/e-magyar/test_input/mnsz2_radio_1mio.tok.test test-tokenizedinput-morph-tag > out.1mio.tokenizedinput-morph-tag
```

```bash
view out.1mio.tokenizedinput-morph-tag
```

To test the guesser, type:

```bash
make RAWINPUT=test_input/halandzsa.test test-morph-tag > out.halandzsa.morph-tag
view out.halandzsa.morph-tag
```

The guesser also seems to work. :)

-----

# Work in progress

_WARNING:_ Everything below is at most in beta
(or just a plan which may be realized or not).
Things below may break without further notice!

for __MILESTONE#2__ (might be completed in 2018):

`emToken`

`DepTool`, `emDep`, maybe: `emChunk`, `emNer`, and even possibly: `emCons`

for __MILESTONE#3__ (might be completed in 2018):

### tsvAPI2.0

The change in a nutshell is:
<br/>
tsvAPI1.0 = `a | b | c` -> tsvAPI2.0 = `e -a | e -b | e -c` = `e -a,b,c`
<br/>
Instead of calling different modules,
we call a central controller (?) and give the modules to run as parameters,
even together in one step.

Expandability:
the module should be added to personalities.py and that's all.
<br/>
(XXX personalities.py could be called config.py)
<br/>
(XXX TODO tutorial for creating a new module)

### REST API -- tsvAPI2.0

To start the server of the pipeline (tsdAPI2.0), use:

```bash
	# for the whole pipeline using tsvAPI2.0
	python3 ./emTSV20.py
```

The tsvAPI2.0 can be called with the URL scheme below where __command__ can be composed arbitrarily off the following modules separated by /:

- morph
- pos
- deptool
- chunk
- dep

Example URLs:

- http://127.0.0.1:5000/morph
- http://127.0.0.1:5000/morph/pos
- http://127.0.0.1:5000/morph/pos/deptool/dep
- http://127.0.0.1:5000/deptool/dep

for __SOMEDAY__:

 - Python library (under [Usage](#usage)) -- as a third use mode
besides CLI and REST API.
 - `--pipe` XOR `--rest`

