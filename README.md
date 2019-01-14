
<!--
 - M#2-nek megfelelő README.md legyen =
maradjunk meg a production release-re (jelenleg ez a MILESTONE#2)
vonatkozó infók közlésénél,
minden, ami azon túl van, az legyen a
[Work in progress](#work-in-progress)
részben (jövőbeli MILESTONE-ok szerint).
-->

# emtsv

__e-magyar__ text processing system -- new version

 * new architecture: inter-module communication via tsv format
 * easy to use command-line interface
 * convenient REST API
 * implemented in Python

 __XXX Jan 2019 MILESTONE#2 (production)__ =
`xtsv` tsv-handling framework finalized.
Tokenization + morphological analysis + POS tagging
(emToken + emMorph + emLem + emTag) tested and work.
Also on a 100.000 word chunk of text.
<!-- XXX See commit: abfbc4bcabfa1b73ad1987e7ef0c5f9007aeca26 -->

If a bug is found please leave feedback with the exact details.

If you use __emtsv__,
please cite the following former articles
(while our new paper is in preparation):

    Váradi Tamás, Simon Eszter, Sass Bálint, Mittelholcz Iván, Novák Attila, Indig Balázs: E-magyar – A Digital Language Processing System. In: Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018), 1307-1312.

    Váradi Tamás, Simon Eszter, Sass Bálint, Gerőcs Mátyás, Mittelholcz Iván, Novák Attila, Indig Balázs, Prószéky Gábor, Farkas Richárd, Vincze Veronika: Az e-magyar digitális nyelvfeldolgozó rendszer. In: MSZNY 2017, XIII. Magyar Számítógépes Nyelvészeti Konferencia, Szeged: Szegedi Tudományegyetem Informatikai Tanszékcsoport, 49-60.

This system is a replacement for the original
https://github.com/dlt-rilmta/hunlp-GATE system.


## Requirements

- GIT LFS
- Python 3.5 <=
- HFST 3.13 <=
- OpenJDK 8
- An UTF-8 locale must be set.

_Remarks:_
<br/>
On Ubuntu 18.04, for installing HFST an `apt-get install hfst` is enough,
as HFST 3.13 is the default is this version.
<br/>
We encountered problems using OpenJDK 11 (#1),
so we recommend using OpenJDK 8.


## Installation

Clone together with submodules (it takes about 3 minutes):

`git lfs clone --recurse-submodules https://github.com/dlt-rilmta/emtsv`

_Note:_ please, ignore the deprecation warning.
(GIT LFS is necessary for properly cloning `emtsv`.
This command checks and ensures that GIT LFS is installed and working.)

Install `Cython` for `emdeppy` (it must be installed in a separate step):

`pip3 install Cython`

Then install requirements for submodules:

`pip3 install -r emmorphpy/requirements.txt`

`pip3 install -r purepospy/requirements.txt`

`pip3 install -r emdeppy/requirements.txt`

`pip3 install -r HunTag3/requirements.txt`

Then download `emToken` binary:

`make -C emtokenpy/ all`


## Creating a Docker image

Use the following recipe as _Dockerfile_:

    FROM ubuntu:18.04

    WORKDIR /app

    # Add curl here
    RUN apt-get -y update && apt-get -y install openjdk-8-jdk hfst python3 python3-pip git curl wget

    # Install git-lfs repo
    RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash

    # Install git-lfs
    RUN apt-get -y install git-lfs

    # Use git lfs for clone to make the process foolproof
    RUN git lfs clone --recurse-submodules https://github.com/dlt-rilmta/emtsv .

    RUN pip3 install Cython
    RUN pip3 install -r emmorphpy/requirements.txt
    RUN pip3 install -r purepospy/requirements.txt
    RUN pip3 install -r emdeppy/requirements.txt
    RUN pip3 install -r HunTag3/requirements.txt

    # Install locales. Any UTF-8 locale will do.
    RUN apt-get -y install locales
    RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
    ENV LANG en_US.UTF-8
    ENV LANGUAGE en_US:en
    ENV LC_ALL en_US.UTF-8

    RUN make -C emtokenpy/ all

    RUN echo "A kutya elment sétálni." > inputfile
    CMD ["make", "RAWINPUT=inputfile", "test-morph-tag-single"]


## Usage

### Command-line interface

```bash
echo "A kutya elment sétálni." | python3 ./emtsv.py tok,morph,pos
```

That's it. :)

The above simply calls `emtsv.py` with the parameter `tok,morph,pos`
and gives the input on stdin.
Using the `xtsv` tsv-handling framework only this has to be done:
call the central controller and give the modules to run as parameters.
Modules are defined in `config.py`.
Modules can be run together or one-by-one,
so the following two approaches give the same result:
`python3 emtsv.py tok,morph` and
`python3 emtsv.py tok | python3 emtsv.py morph`.
This is possible thank to the standardized inter-module communication
via tsv (with appropriate headers).
To extend the toolchain is straightforward:
add new modules to `config.py` and that's all.

### REST API

To start the server, use `emtsv.py` without any parameters
(it takes a few minutes):

```bash
python3 ./emtsv.py
```

When the server outputs a message like `* Running on`
then it is ready to accept requests.

To use the started server, clients should call it this way from Python:

```python
>>> import requests
>>> r = requests.post('http://127.0.0.1:5000/tok/morph/pos', files={'file':open('test_input/input.test', encoding='UTF-8')})
>>> print(r.text)
...
```

The `tok/morph/pos` part of the URL are the modules to run,
separated by `/`.
This part can be composed from the modules defined in `config.py`.
The server checks whether all necessary data columns are availabe
at each point between two modules, and gives an error message
if there are any problems.

The format of the input file or stream
(`test_input/input.test` in this case)
must comply to the __emtsv__ standards (header, column names, etc.)
and must contain every necessary data columns for the first module to run,
as for the CLI version.
Please consult the examples in `test_output` directory for guidance.

Running the first request can take more time (a few minutes)
as the server loads some models then.


## Toolchain

[Current toolchain](doc/emtsv_modules.pdf) in a figure.


## Testing

### Command-line interface

To automatically check that everything is ok
with the command-line interface simply run:

```bash
./test.sh
```

Or go through the following steps manually:

```bash
time make test-tok-morph > out.input.tok-morph
time make test-tok-morph-tag > out.input.tok-morph-tag
time make test-tok-morph-tag-single > out.input.tok-morph-tag-single
tkdiff out.input.tok-morph out.input.tok-morph-tag
diff out.input.tok-morph-tag out.input.tok-morph-tag-single
```

The first diff shows the result of POS tagging.
<br/>
The second diff outputs nothing = the two files are the same:
`make test-tok-morph-tag` runs the modules separately
connected to each other by unix pipes, while 
`make test-tok-morph-tag-single` runs the same modules in one step.

(Please note that there is a warning during normal operation:
"PyJNIus is already imported with the following classpath: ...")

To test the guesser, type:

```bash
make RAWINPUT=test_input/halandzsa.test test-tok-morph-tag > out.halandzsa.tok-morph-tag
view out.halandzsa.tok-morph-tag
```

The guesser also seems to work. :)

There are also some larger pre-tokenized testfiles available locally
(on juniper) for development staff, see `Makefile`.
<br/>
This command processes a 100 thousand words chunk of text
(can take about 3 minutes to run):

```bash
time make RAWINPUT=/store/projects/e-magyar/test_input/hundredthousandwords.txt test-tok-morph-tag > out.100.tok-morph-tag
```

To investigate the results:

```bash
view out.100.tok-morph-tag
```

### REST API

To check that everything is ok
with the REST API, start the server first and then run:

```bash
./testrest.sh
```


## Troubleshooting

Below are some common error messages and for what reasons they usually appear.

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

- Errors like below is because the classpath in `jnius_config.get_classpath()` is not set properly.
Use `jnius_config.add_classpath(PATH)` to add the missing path to classpath.

```Python
Traceback (most recent call last):
  File "/app/emtsv.py", line 60, in <module>
    inited_tools = init_everything(tools)
  File "/app/xtsv/pipeline.py", line 32, in init_everything
    current_initialised_tools[prog_name] = prog(*prog_args, **prog_kwargs)  # Inint programs...
  File "/app/emdeppy/emdeppy/emdeppy.py", line 56, in __init__
    self._parser = self._autoclass('is2.parser.Parser')(self._jstr(model_file.encode('UTF-8')))
  File "/usr/local/lib/python3.5/dist-packages/jnius/reflect.py", line 159, in autoclass
    c = find_javaclass(clsname)
  File "jnius/jnius_export_func.pxi", line 26, in jnius.find_javaclass (jnius/jnius.c:17089)
jnius.JavaException: Class not found b'is2/parser/Parser'
```

## Work in progress

_WARNING:_ Everything below is at most in beta
(or just a plan which may be realized or not).
Things below may break without further notice!

for __MILESTONE#3__ (might be completed in 2019 Q1):

`DepTool`, `emDep`, maybe: `emChunk`, `emNer`, and even possibly: `emCons`

for __SOMEDAY__:

 - Python library (under [Usage](#usage)) -- as a third use mode
besides CLI and REST API.
 - `--pipe` XOR `--rest`

 - XXX TODO tutorial for creating a new module

