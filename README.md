
<!--
 - M#2-nek megfelelő README.md legyen =
maradjunk meg a production release-re (jelenleg ez a MILESTONE#2)
vonatkozó infók közlésénél,
minden, ami azon túl van, az legyen a
[Work in progress](#work-in-progress)
részben (jövőbeli MILESTONE-ok szerint).
B) Vagy csináljunk egy linket a megfelelő kommitra, ami a MILESTONE#X README.md-t mutatja.
Ezért hülyeség lenne kétszer dokumentálni a dolgokat.
C) branch-be fejlesztünk és a MILESTONE-oknál merge-lünk.
-->

# __e-magyar__ text processing system (emtsv)

- inter-module communication via the [`xtsv` framework](https://github.com/dlt-rilmta/xtsv)
    - processing can be started or stopped at any module
    - module dependency checks before processing
    - easy to add new modules
    - multiple alternative modules for some task
- easy to use command-line interface
- convenient REST API with simple web frontend
- Python library API
- Docker image, and runnable Docker form

 __17 Sep 2019 MILESTONE#4 (production)__ =
xtsv and dummyTagger separated, UDPipe, Hunspell added,
many API breaks compared to the previous milestone,
Runnable Docker image, dropped DepToolPy, and many more changes.

If a bug is found please leave feedback with the exact details.

## Citing and License

If you use __emtsv__, please cite the following articles:

    Indig Balázs, Sass Bálint, Simon Eszter, Mittelholcz Iván, Kundráth Péter, Vadász Noémi. emtsv – Egy formátum mind felett. In: Berend Gábor, Gosztolya Gábor, Vincze Veronika (szerk.): MSZNY 2019, XV. Magyar Számítógépes Nyelvészeti Konferencia (MSZNY 2019). Szeged: Szegedi Tudományegyetem Informatikai Tanszékcsoport, 235-247.

    Váradi Tamás, Simon Eszter, Sass Bálint, Mittelholcz Iván, Novák Attila, Indig Balázs: E-magyar – A Digital Language Processing System. In: Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018), 1307-1312.

    Váradi Tamás, Simon Eszter, Sass Bálint, Gerőcs Mátyás, Mittelholcz Iván, Novák Attila, Indig Balázs, Prószéky Gábor, Farkas Richárd, Vincze Veronika: Az e-magyar digitális nyelvfeldolgozó rendszer. In: MSZNY 2017, XIII. Magyar Számítógépes Nyelvészeti Konferencia, Szeged: Szegedi Tudományegyetem Informatikai Tanszékcsoport, 49-60.

This system is a replacement for the original https://github.com/dlt-rilmta/hunlp-GATE system.

``emtsv`` is licensed under the LGPL 3.0 license. The submodules have their own license.

## Requirements

- GIT LFS (See notes)
- Python 3.5 <=
- HFST 3.13 <=
- Hunspell (libhunspell-dev, hunspell-hu) 1.6.2 <=
- OpenJDK 8 JDK (not JRE)
- An UTF-8 locale must be set.

## Installation

- From the git repository: see [detailed instructions](doc/installation.md) in the documentation
- From __prebuilt Docker image__ ([https://hub.docker.com/r/mtaril/emtsv](https://hub.docker.com/r/mtaril/emtsv)):
    ```bash
    docker pull mtaril/emtsv:latest
    ```
    - See [detailed instructions](doc/installation.md) for building the _Docker image_

## Usage

Here we present the usage scenarios. The individual modules are documented in details below. 
To extend the toolchain with new modules just add new modules to `config.py`.

### Command-line interface

- Multiple modules at once:
    ```bash
    echo "A kutya elment sétálni." | python3 ./main.py tok,spell,morph,pos,conv-morph,dep,chunk,ner
    ```
- Each modules _glued together_ with the standard *nix pipelines where user can interact with the data between the modules:
     ```bash
     echo "A kutya elment sétálni." | \
        python3 main.py tok | \
        python3 main.py spell | \
        python3 main.py morph | \
        python3 main.py pos | \
        python3 main.py conv-morph | \
        python3 main.py dep | \
        python3 main.py chunk | \
        python3 main.py ner
     ```
- `emtsv` can also used with inputs and outputs redirected or with string input (also applies to runnabble docker form):
    ```bash
    python3 ./main.py tok,spell,morph,pos,conv-morph,dep,chunk,ner -i input.txt -o output.txt
    python3 ./main.py tok,spell,morph,pos,conv-morph,dep,chunk,ner --text "A kutya elment sétálni."
    ```

### __Docker image__

- Runnable docker form (CLI usage of docker image):
    ```bash
    cat input.txt | docker run -i mtaril/emtsv tok,morph,pos > output.txt
    ```
- As service through Rest API (docker container)
    ```bash
    docker run --rm -p5000:5000 -it mtaril/emtsv  # REST API
    ```

### REST API

Server:
- Debug server (Flask) __only for development (single threaded, one request a time)__:
    ```bash
    # Without parameters!
    python3 ./main.py
    ```
    When the server outputs a message like `* Running on` then it is ready to accept requests on http://127.0.0.1:5000 .
    (__We do not recommend using this method in production as it is built atop of Flask debug server! Please consider using the Docker image for REST API in production!__)
- Any wsgi server (`uwsgi`, `gunicorn`, `waitress`, etc.) can be configured to run with [docker/emtsvREST.wsgi](docker/emtsvREST.wsgi) .
- Docker image (see above)

Client:
- Web fronted provided by `xtsv`
- From Python (the URL contains the tools to be run separated by `/`):
    ```python
    >>> import requests
    >>> # With input file
    >>> r = requests.post('http://127.0.0.1:5000/tok/morph/pos', files={'file': open('tests/test_input/input.test', encoding='UTF-8')})
    >>> print(r.text)
    ...
    >>> # With input text
    >>> r = requests.post('http://127.0.0.1:5000/tok/morph/pos', data={'text': 'A kutya elment sétálni.'})
    >>> print(r.text)
    ...
    >>> # CoNLL style comments can be enabled per request (disabled by default):
    >>> r = requests.post('http://127.0.0.1:5000/tok/morph/pos', files={'file':open('tests/test_input/input.test', encoding='UTF-8')}, data={'conll_comments': True})
    >>> print(r.text)
    ...
    ```
    The server checks whether the module order is feasible, and gives an error message if there are any problems.

### As Python Library

1. Install emtsv in `emtsv` directory or make sure the emtsv installation is in the `PYTHONPATH` environment variable
2. `import emtsv`
3. Example:
    ```Python
    import sys
    from emtsv import build_pipeline, jnius_config, tools, presets, process, pipeline_rest_api, singleton_store_factory
    
    jnius_config.classpath_show_warning = False  # To suppress warning
    
    # Imports end here. Must do only once per Python session
    
    # Set input from any stream or iterable and output stream...
    input_data = sys.stdin
    output_iterator = sys.stdout
    # Raw, or processed TSV input list and output file...
    # input_data = iter(['Raw text', 'line-by-line'])
    # input_data = iter([['form', 'xpostag'], ['Header', 'NNP'], ['then', 'RB'], ['tokens', 'VBZ'], ['line-by-line', 'NN'], ['.', '.']])
    # output_iterator = open('output.txt', 'w', encoding='UTF-8')
    # Or use string
    # input_data = 'Raw text as string.'
    
    # Select a predefined task to do or provide your own list of pipeline elements
    used_tools = ['tok', 'morph', 'pos']
   
    conll_comments = True  # Enable the usage of CoNLL comments
   
    # Run the pipeline on input and write result to the output...
    output_iterator.writelines(build_pipeline(input_data, used_tools, tools, presets, conll_comments))
    
    # Alternative: Run specific tool for input streams (still in emtsv format).
    # Useful for training a module (see Huntag3 for details):
    # output_iterator.writelines(process(input_data, inited_tool))
    
    # Or process individual tokens further... WARNING: The header will be the first item in the iterator!
    # for tok in build_pipeline(input_data, used_tools, tools, presets, conll_comments):
    #     if len(tok) > 1:  # Empty line (='\n') means end of sentence
    #         form, xpostag, *rest = tok.strip().split('\t')  # Split to the expected columns
    
    # Alternative2: Flask application (REST API)
    singleton_store = singleton_store_factory()
    app = application = pipeline_rest_api(name='e-magyar-tsv', available_tools=tools, presets=presets,
                                conll_comments=conll_comments, singleton_store=singleton_store,
                                form_title='e-magyar text processing system',
                                doc_link='https://github.com/dlt-rilmta/emtsv')
    # And run the Flask debug server separately
    app.run()
    ```

__API documentation for `emtsv`__:
- `ModuleError`: The exception throwed when something bad happened with the modules (eg. Module could not be found or the ordering of the modules is not feasible because the required and supplied fields)
- `HeaderError`: The exception throwed when the input could not satisfy the required fields in its header
- `jnius_config`: Set JAVA VM options and CLASSPATH for the PyJNIus library
- `tools`: The dictionary of tools (see [configuration](#configuration) for details)
- `presets`: The dictionary of shorthands for tasks which are defined as list of tools to be run in a pipeline (see [configuration](#configuration) for details)
- `build_pipeline(inp_data, used_tools, available_tools, presets, conll_comments=False) -> iterator_on_output_lines`: Build the current pipeline from the input data (stream, iterable or string), the list of the elements of the desired pipeline chosen from the available tools and presets returning an output iterator.
- `pipeline_rest_api(name, available_tools, presets, conll_comments, singleton_store=None, form_title, doc_link) -> app`: Creates a Flask application with the REST API and web frontend on the available initialised tools and presets with the desired name. Run with a wsgi server or Flask's built-in server with with `app.run()` (see [REST API section](#REST API))
- `singleton_store_factory() -> singleton`: Singletons can used for initialisation of modules (eg. when the application is restarted frequently and not all modules are used between restarts)
- `process(stream, internal_app, conll_comments=False) -> iterator_on_output_lines`: A low-level API to run a specific member of the pipeline on a specific input, returning an output iterator
- `parser_skeleton(...) -> argparse.ArgumentParser(...)`: A CLI argument parser skeleton can be further customized when needed 
- `add_bool_arg(parser, name, help_text, default=False, has_negative_variant=True)`: A helper function to easily add BOOL arguments to the ArgumentParser class
- `download(available_models=None, required_models=None)`: Download (a subset of) all large model files specified in models.yaml (filename can be changed in the first parameter)

## Data format

The input and output can be one of the following:
- Free form text file
- TSV file with fixed column order and without header (like CoNLL-U)
- TSV file with arbitrary column order where the columns are identified by the TSV header (main format of `xtsv`)

The TSV files are formated as follows (closely resembling the CoNLL-U, vertical format):
- The first line is the header (when the column order is not fixed and known by the next module)
- Sentences are separated by emtpy lines
- If allowed by configuration, zero or more comment lines (eg. lines starts with hashtag and space) immediately preceedes sentences
- One token per line (one column), the other columns contain the information on that individual token
- Columns are separated by TAB characters

The fields are identified by the header in the first line of the input. Each module can (but not necessarily) define:
- A set of source fields which is required to present in the input
- A list of target fields which are to be generated to the output in order

Newly generated fields are started from the right of the rightmost column, the existing columns should not be modified.

The following types of modules can be defined by their input and output format requirements:
    
- __Tokeniser__: No source fields, no header, has target fields, free-format text as input, TSV+header output
- __Internal module__: Has source fields, has header, has target fields, TSV+header input, TSV+header output
- __Finalizer__: Has source fields, no header, no target fields, TSV+header input, free-format text as output
- __Fixed-order TSV importer__: No source fields, no header, has target fields, Fixed-order TSV w/o header as input, TSV+header output
- __Fixed-order TSV processor__: No source fields, no header, no target fields, Fixed-order TSV w/o header as input, Fixed-order TSV w/o header as output

Please consult the examples in `tests/test_input` and `tests/test_output` directory for further guidance.

## Modules

Modules are defined in `config.py`. The current toolchain is consists of the following modules (See [the topology of the current toolchain](doc/emtsv_modules.pdf) for an overview) can be called by their name (or using their shorthand names in brackets):

- `emToken` (`tok`): Tokenizer
- `emMorph` (`morph`): Morphological analyser together with emLem lemmatiser
- `hunspell` (`spell`): Spellchecker, stemmer and morphological analyser
- `emTag` (`pos`): POS-tagger
- `emChunk` (`chunk`): Maximal NP-chunker
- `emNER` (`ner`): Named-entity recogniser
- `emmorph2ud` (`conv-morph`): Converter from emMorph code to UD upos and feats format
- `emDep` (`dep`): Dependency parser
- `emCons` (`cons`): Constituent parser
- `emCoNLL` (`conll`): Converter from emtsv to CoNLL-U format
- `emDummy` (`dummy-tagger`): Example module
- `udpipe-tok`: The UDPipe tokeniser
- `udpipe-pos`: The UDPipe POS-tagger
- `udpipe-parse`: The UDPipe depenceny parser
- `udpipe-pos-parse`: From POS-tagging to dependency parsing in 'one step' with UDPipe, roughly (!) same as `udpipe-pos,udpipe-parse`
- `udpipe-tok-parse`: From tokenisation to dependency parsing in 'one step' with UDPipe, roughly (!) same as `udpipe-tok,udpipe-pos,udpipe-parse`
- `udpipe-tok-pos`: From tokenisation to POS-tagging in 'one step' with UDPipe, roughly (!) same as `udpipe-tok,udpipe-pos`

The following presets are defined as shorthand for the common tasks:

- `analyze`: Run the full pipeline, same as: `emToken,emMorph,emTag,emChunk,emNER,emmorph2ud,emDep-ud,emCons`
- `tok-morph`: From tokenisation to morphological analysis, same as `emToken,emMorph`
- `tok-pos`: From tokenisation to POS-tagging, same as `emToken,emMorph,emTag`
- `tok-chunk`: From tokenisation to maximal NP-chunking, same as `emToken,emMorph,emTag,emChunk`
- `tok-ner`: From tokenisation to named-entity recognition, same as `emToken,emMorph,emTag,emNER`
- `tok-udpos`: From tokenisation to POS-tagging in UD format, same as `emToken,emMorph,emTag,emmorph2ud`
- `tok-dep`: From tokenisation to dependency parsing, same as `emToken,emMorph,emTag,emmorph2ud,emDep-ud`
- `tok-cons`: From tokenisation to constituent parsing, same as `emToken,emMorph,emTag,emCons`

### Example
The examples presented above simply call `main.py` with the parameter `tok,spell,morph,pos,conv-morph,dep,chunk,ner` takes the input on STDIN and gives out in STDOUT.
We use here a tokenizer, a morphological analyzer, a POS tagger, a morphology converter, a dependency parser, a chunker and a named entity recognizer.
(The converter is needed as the POS tagger and the dependency parser works with different morphological coding systems.)

### Creating a module

The following requirements apply for a new module:

1) It must provide (at least) the mandatory API (see [emDummy](https://github.com/dlt-rilmta/emdummy) for a well-documented example)
2) It must conform to the field-name conventions of emtsv and the format conventions of [xtsv](https://github.com/dlt-rilmta/xtsv)
3) It must have an LGPL 3.0 compatible lisence

The following steps are needed to insert the new module into the pipeline:

1) Add the new module as submodule to the repository
2) Insert the configuration in `config.py`:

    ```python
    # c) # Setup the tuple: module name (ending with the filename the class defined in),
    #       class, friendly name, args (tuple), kwargs (dict)
    em_dummy = ('emdummy.dummytagger', 'DummyTagger', 'EXAMPLE (The friendly name of DummyTagger used in REST API form)',
            ('Params', 'goes', 'here'),
            {'source_fields': {'Source field names'}, 'target_fields': ['Target field names']})
    ```

3) Add the new module to `tools` list in `config.py`, optionally also to `presets` dictionary
    ```python
       tools = [...,
                (em_dummy, ('dummy-tagger', 'emDummy')),
                ]
    ```
4) Test, commit and push

<!--
## Work in progress

_WARNING:_ Everything below is at most in beta
(or just a plan which may be realized or not).
Things below may break without further notice!

for __SOMEDAY__:

 - `emCons` (works but rather slow)
 - `CoNLL-U importer`
-->

## Further documentation

- [installation](doc/installation.md)
- [testing](doc/testing.md)
- [troubleshooting](doc/troubleshooting.md)
