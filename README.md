
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

 __19 Feb 2019 MILESTONE#3 (production)__ =
tokenization, morphological analysis, POS tagging,
dependency parsing, chunking and named entity recognition
(emToken + emMorph + emLem + emTag + emDep + emChunk + emNer)
tested and work.
Also on a 100.000 word chunk of text.

If a bug is found please leave feedback with the exact details.

If you use __emtsv__,
please cite the following articles:

    Indig Balázs, Sass Bálint, Simon Eszter, Mittelholcz Iván, Kundráth Péter, Vadász Noémi. emtsv – Egy formátum mind felett. In: Berend Gábor, Gosztolya Gábor, Vincze Veronika (szerk.): MSZNY 2019, XV. Magyar Számítógépes Nyelvészeti Konferencia (MSZNY 2019). Szeged: Szegedi Tudományegyetem Informatikai Tanszékcsoport, 235-247.

    Váradi Tamás, Simon Eszter, Sass Bálint, Mittelholcz Iván, Novák Attila, Indig Balázs: E-magyar – A Digital Language Processing System. In: Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018), 1307-1312.

    Váradi Tamás, Simon Eszter, Sass Bálint, Gerőcs Mátyás, Mittelholcz Iván, Novák Attila, Indig Balázs, Prószéky Gábor, Farkas Richárd, Vincze Veronika: Az e-magyar digitális nyelvfeldolgozó rendszer. In: MSZNY 2017, XIII. Magyar Számítógépes Nyelvészeti Konferencia, Szeged: Szegedi Tudományegyetem Informatikai Tanszékcsoport, 49-60.

This system is a replacement for the original
https://github.com/dlt-rilmta/hunlp-GATE system.


## Requirements

- GIT LFS
- Python 3.5 <=
- HFST 3.13 <=
- OpenJDK 8 JDK (not JRE)
- An UTF-8 locale must be set.

_Remarks:_
<br/>
On Ubuntu 18.04, for installing HFST an `apt-get install hfst` is enough,
as HFST 3.13 is the default is this version.
<br/>
We encountered problems using OpenJDK 11 (#1),
so we recommend using OpenJDK 8.
<br/>
On Ubuntu 18.04, for installing OpenJDK 8 JDK an `apt-get install openjdk-8-jdk` is enough.
<br/>
On Ubuntu 18.04, UTF-8 locale is set by default. Can be checked typing `locale` in the terminal. (Lines end with '.UTF-8')
<br/>
## Installation

Clone together with submodules (it takes about 3 minutes):

`git lfs clone --recurse-submodules https://github.com/dlt-rilmta/emtsv`

_Note:_ please, ignore the deprecation warning.
(GIT LFS is necessary for properly cloning `emtsv`.
This command checks and ensures that GIT LFS is installed and working.)
<br/>
_Note2:_ If you are certain about GIT LFS is installed, you can use: `git clone` to avoid the warning. (This command also works without GIT LFS installed, but as the model files will not be downloaded emtsv might not work. See [Troubleshooting](#troubleshooting) section for details.)
<br/>

Install `Cython` for `emdeppy` (it must be installed in a separate step before `PyJNIus`):

`pip3 install Cython`

Then install requirements for submodules:

`pip3 install -r emmorphpy/requirements.txt`

`pip3 install -r purepospy/requirements.txt`

`pip3 install -r emdeppy/requirements.txt`

`pip3 install -r HunTag3/requirements.txt`

Then download `emToken` binary:

`make -C emtokenpy/ all`

## __Docker image__

emtsv can be used with docker through the command-line and REST API interfaces

- with the provided `Dockerfile` (see `docker` folder):
    ```bash
    docker build -t emtsv:stable .
    docker run --rm -p5000:5000 -it emtsv:stable  # REST API
    cat input.txt | docker run -i emtsv:stable tok,morph,pos > output.txt
    ```

- with prebuilt __Docker image__ from [https://hub.docker.com/r/mtaril/emtsv](https://hub.docker.com/r/mtaril/emtsv):
    ```bash
    docker pull mtaril/emtsv:latest
    docker run --rm -p5000:5000 -it mtaril/emtsv  # REST API
    cat input.txt | docker run -i mtaril/emtsv tok,morph,pos > output.txt
    ```

## Usage

### Command-line interface

```bash
echo "A kutya elment sétálni." | python3 ./emtsv.py tok,morph,pos,conv-morph,dep,chunk,ner
```

That's it. :)

The above simply calls `emtsv.py` with the parameter
`tok,morph,pos,conv-morph,dep,chunk,ner`
and gives the input on stdin.
Using the `xtsv` tsv-handling framework only this has to be done:
call the central controller and give the modules to run as parameters.
Modules are defined in `config.py`.
We use here a tokenizer, a morphological analyzer, a POS tagger,
a morphology converter, a dependency parser, a chunker
and a named entity recognizer.
(The converter is needed as the POS tagger and the dependency parser
 works with different morphological coding systems.) 
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
<br/>
(__We do not recommend using this method in production as it is built atop of Flask debug server! Please consider using the Docker image for REST API in production!__)

To use the started server, clients should call it this way from Python:

```python
>>> import requests
>>> r = requests.post('http://127.0.0.1:5000/tok/morph/pos', files={'file':open('test_input/input.test', encoding='UTF-8')})
>>> print(r.text)
...
>>> # Or with CoNLL style comments enabled:
>>> r = requests.post('http://127.0.0.1:5000/tok/morph/pos', files={'file':open('test_input/input.test', encoding='UTF-8')}, data={'conll_comments': True})
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

### As Python Library

1. Install emtsv in `emtsv` directory or make sure the emtsv installation is in the `PYTHONPATH` environment variable
2. `import emtsv`
3. Now you have the following API under `emtsv`
    - `jnius_config`: Set JAVA VM options and CLASSPATH for the PyJNIus library for the modules (see `config.py` for example usage)
    - `tools`: The dictionary of tools where different names are used as keys and raw classes (to be initialised) are used as values
    - `presets`: The dictionary of shorthands for tasks which are defined as list of tools to be run in a pipeline
    - `init_everything(available_tools, init_singleton=None) -> inited_tools`: Init the (arbitrarily chosen subset of) available tools defined `config.py` and stored in `tools` variable returns the dictionary of inited tools
    - `build_pipeline(inp_stream, used_tools, available_tools, presets, conll_comments=False) -> iterator_on_output_lines`: Build the current pipeline from the input stream, the list of the elements of the desired pipeline chosen from the available initialised tools and presets returning an output iterator.
    - `pipeline_rest_api(name, available_tools, presets, conll_comments) -> app`: Creates a Flask application with the REST API on the available initialised tools and presets with the desired name. Run Flask's built-in server with with `app.run()` (__It is not recommended for production!__)
    - `process(stream, internal_app, conll_comments=False) -> iterator_on_output_lines`: A low-level API to run a specific member of the pipeline on a specific input, returning an output iterator
    - `parser_skeleton(...) -> argparse.ArgumentParser(...)`: A CLI argument parser skeleton can be further customized when needed 
    - `add_bool_arg(parser, name, help_text, default=False)`: A helper function to easily add BOOL arguments to the ArgumentParser class

Example:

```Python
import sys

from emtsv import init_everything, build_pipeline, jnius_config, tools, presets, process, pipeline_rest_api

jnius_config.classpath_show_warning = False  # To suppress warning

# Imports end here. Must do only once per Python session

# Set input and output iterators...
input_iterator = sys.stdin
output_iterator = sys.stdout

# Raw, or processed TSV input list and output file...
# input_iterator = iter(['Raw text', 'line-by-line'])
# input_iterator = iter([['form', 'xpostag'], ['Header', 'NNP'], ['then', 'RB'], ['tokens', 'VBZ'], ['line-by-line', 'NN'], ['.', '.']])
# output_iterator = open('output.txt', 'w', encoding='UTF-8')

# Select a task to do or provide your own list of pipeline elements
used_tools = presets['tok-dep']

# Init the selected tools
inited_tools = init_everything({k: v for k, v in tools.items() if k in set(used_tools)})

# Run the pipeline on input and write result to the output...
output_iterator.writelines(build_pipeline(input_iterator, used_tools, inited_tools, presets))

# Alternative: Run specific tool for input (still in emtsv format):
output_iterator.writelines(process(input_iterator, inited_tools['morph']))

# Or process individual tokens further... WARNING: The header will be the first item in the iterator!
# for tok in build_pipeline(input_iterator, used_tools, inited_tools, presets):
#     if len(tok) > 1:  # Empty line (='\n') means end of sentence
#         form, xpostag, *rest = tok.strip().split('\t')  # Split to the expected columns

# Alternative2: Run REST API debug server
app = pipeline_rest_api('TEST', inited_tools, presets,  False)
app.run()
```

## Toolchain

The current toolchain is consists of the following modules can be called by their name (or using their shorthand names in brackets):

- `emToken` (`tok`): Tokenizer
- `emMorph` (`morph`): Morphological analyser together with emLem lemmatiser
- `emTag` (`pos`): POS-tagger
- `emChunk` (`chunk`): Maximal NP-chunker
- `emNER` (`ner`): Named-entity recogniser
- `emmorph2ud` (`conv-morph`): Converter from emMorph code to UD upos and feats format
- `emDep-ud` (`dep`): Dependency parser
- `emCons` (`cons`): Constituent parser
- `emCoNLL` (`conll`): Converter from emtsv to CoNLL-U format
- `emDummy` (`dummy-tagger`): Example module

The following presets are defined as shorthand for the common tasks:

- `analyze`: Run the full pipeline, same as: `emToken,emMorph,emTag,emChunk,emNER,emmorph2ud,emDep-ud,emCons`
- `tok-morph`: From tokenisation to morphological analysis, same as `emToken,emMorph`
- `tok-pos`: From tokenisation to POS-tagging, same as `emToken,emMorph,emTag`
- `tok-chunk`: From tokenisation to maximal NP-chunking, same as `emToken,emMorph,emTag,emChunk`
- `tok-ner`: From tokenisation to named-entity recognition, same as `emToken,emMorph,emTag,emNER`
- `tok-udpos`: From tokenisation to POS-tagging in UD format, same as `emToken,emMorph,emTag,emmorph2ud`
- `tok-dep`: From tokenisation to dependency parsing, same as `emToken,emMorph,emTag,emmorph2ud,emDep-ud`
- `tok-cons`: From tokenisation to constituent parsing, same as `emToken,emMorph,emTag,emCons`


See [the topology of the current toolchain](doc/emtsv_modules.pdf) for an overview.


## Creating a module

The following requirements apply for a new module:

1) It must provide (at least) the mandatory API (see [emDummy](https://github.com/dlt-rilmta/emdummy) for a well-documented example)
2) It must conform to the field-name conventions of emtsv and the format conventions of xtsv
3) It must have an LGPL 3.0 compatible lisence

The following steps are needed to insert the new module into the pipeline:

1) Add the new module as submodule to the repository
2) Insert the configuration in `config.py`:

    ```python
    # a) Add to path if needed
    sys.path.append(os.path.join(os.path.dirname(__file__), 'emdummy'))
    # b) Import the class
    from emdummy.dummy import DummyTagger

    # c) Setup the triplet: class, args (tuple), kwargs (dict)
    em_dummy = (DummyTagger, ('Params', 'goes', 'here'),
                {'source_fields': {'Source field names'}, 'target_fields': ['Target field names']})
    ```

3) Add the new module to `tools` dict in `config.py`, optionally also to `presets` dictionary
4) Test, commit and push


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

(Please note that there can be a warning during normal operation:
"PyJNIus is already imported with the following classpath: ...")

To test the guesser, type:

```bash
make RAWINPUT=tests/test_input/halandzsa.test test-tok-morph-tag > out.halandzsa.tok-morph-tag
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

To test the pipeline with all modules up to the named entity recognizer,
type:

```bash
make test-all-single > out.input.all
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

for __SOMEDAY__:

 - `emCons` (works but rather slow)
