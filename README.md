
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

- GIT LFS
- Python 3.5 <=
- HFST 3.13 <=
- OpenJDK 8
- An UTF-8 locale must be set.

_Remarks:_
<br/>
On Ubuntu 18.04, an `apt-get install hfst` is enough,
as HFST 3.13 is the default is this version.
<br/>
We encountered problems using OpenJDK 11 (#1),
so we recommend using OpenJDK 8.

## Install

Clone together with submodules (it takes about 3 minutes):

`git lfs clone --recurse-submodules https://github.com/dlt-rilmta/e-magyar-tsv`

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

# Frequently Asked Questions

- Errors like below is because `JAVA_HOME` environment variable is not set properly.

```Python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.5/site-packages/jnius/__init__.py", line 13, in <module>
    from .reflect import *  # noqa
  File "/usr/lib/python3.5/site-packages/jnius/reflect.py", line 15, in <module>
    class Class(with_metaclass(MetaJavaClass, JavaClass)):
  File "/usr/lib/python3.5/site-packages/six.py", line 827, in __new__
    return meta(name, bases, d)
  File "jnius/jnius_export_class.pxi", line 111, in jnius.MetaJavaClass.__new__
  File "jnius/jnius_export_class.pxi", line 161, in jnius.MetaJavaClass.resolve_class
  File "jnius/jnius_env.pxi", line 11, in jnius.get_jnienv
  File "jnius/jnius_jvm_dlopen.pxi", line 90, in jnius.get_platform_jnienv
  File "jnius/jnius_jvm_dlopen.pxi", line 45, in jnius.create_jnienv
  File "/usr/lib/python3.5/os.py", line 725, in __getitem__
    raise KeyError(key) from None
KeyError: 'JAVA_HOME'
```

- Errors like below is because the JRE version is not compatible.

```Python
Traceback (most recent call last):
  File "/app/emTagREST.py", line 12, in <module>
    prog = tagger(*args, **kwargs)
  File "/app/purepospy/purepospy.py", line 66, in __init__
    self._autoclass = import_pyjnius(PurePOS.class_path)
  File "/app/purepospy/purepospy.py", line 34, in import_pyjnius
    from jnius import autoclass
  File "/usr/lib/python3.7/site-packages/jnius/__init__.py", line 13, in <module>
    from .reflect import *  # noqa
  File "/usr/lib/python3.7/site-packages/jnius/reflect.py", line 15, in <module>
    class Class(with_metaclass(MetaJavaClass, JavaClass)):
  File "/usr/lib/python3.7/site-packages/six.py", line 827, in __new__
    return meta(name, bases, d)
  File "jnius/jnius_export_class.pxi", line 111, in jnius.MetaJavaClass.__new__
  File "jnius/jnius_export_class.pxi", line 161, in jnius.MetaJavaClass.resolve_class
  File "jnius/jnius_env.pxi", line 11, in jnius.get_jnienv
  File "jnius/jnius_jvm_dlopen.pxi", line 90, in jnius.get_platform_jnienv
  File "jnius/jnius_jvm_dlopen.pxi", line 59, in jnius.create_jnienv
SystemError: Error calling dlopen(b'/usr/lib/jvm/default-java/jre/lib/amd64/server/libjvm.so': b'/usr/lib/jvm/default-java/jre/lib/amd64/server/libjvm.so: cannot open shared object file: No such file or directory'
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>
BrokenPipeError: [Errno 32] Broken pipe
```

- Errors like below is due to missing modelfile because `git lfs` is not installed before clone.

```Python
  File "/app/purepospy/purepospy.py", line 168, in tag_sentence
    read_mod = serializer().readModelEx(self._model_jfile)
  File "jnius/jnius_export_class.pxi", line 733, in jnius.JavaMethod.__call__
  File "jnius/jnius_export_class.pxi", line 899, in jnius.JavaMethod.call_staticmethod
  File "jnius/jnius_utils.pxi", line 93, in jnius.check_exception
jnius.JavaException: JVM exception occurred: invalid stream header: 76657273
```

- Errors like below is because no __Unicode-aware locale__ (eg. hu_HU.UTF-8) is set.

```Python
File "/app/emmorphpy/emmorphpy/emmorphpy.py", line 76, in _load_config
props = jprops.load_properties(fp)
File "/usr/lib/python3.6/site-packages/jprops.py", line 43, in load_properties
return mapping(iter_properties(fh))
File "/usr/lib/python3.6/site-packages/jprops.py", line 107, in iter_properties
for line in _property_lines(fh):
File "/usr/lib/python3.6/site-packages/jprops.py", line 271, in _property_lines
for line in _read_lines(fp):
File "/usr/lib/python3.6/site-packages/jprops.py", line 263, in _universal_newlines
for line in lines:
File "/usr/lib/python3.6/encodings/ascii.py", line 26, in decode
return codecs.ascii_decode(input, self.errors)[0]
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc5 in position 603: ordinal not in range(128)
```

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

