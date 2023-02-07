
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

- inter-module communication via the [`xtsv` framework](https://github.com/nytud/xtsv)
    - processing can be started or stopped at any module
    - module dependency checks before processing
    - easy to add new modules
    - multiple alternative modules for some tasks
- easy to use command-line interface
- convenient REST API with simple web frontend
- Python library API
- Docker image and runnable docker form

 __17 Sep 2019 MILESTONE#4 (production)__ =
xtsv and dummyTagger separated, UDPipe, Hunspell added,
many API breaks compared to the previous milestone,
Runnable Docker image, dropped DepToolPy, and many more changes.

If a bug is found please leave feedback with the exact details.

## Citing and License

See [`docs/cite.bib`](docs/cite.bib) for BibTeX entries.

If you use the __emtsv__ system, please cite:

    Simon Eszter, Indig Balázs, Kalivoda Ágnes, Mittelholcz Iván, Sass Bálint, Vadász Noémi. Újabb fejlemények az e-magyar háza táján. In: Berend Gábor, Gosztolya Gábor, Vincze Veronika (szerk.): MSZNY 2020, XVI. Magyar Számítógépes Nyelvészeti Konferencia (MSZNY 2020). Szeged: Szegedi Tudományegyetem Informatikai Tanszékcsoport, 29-42.

    Balázs Indig, Bálint Sass, Eszter Simon, Iván Mittelholcz, Noémi Vadász, and Márton Makrai: One format to rule them all – The emtsv pipeline for Hungarian. In: Proceedings of the 13th Linguistic Annotation Workshop. Association for Computational Linguistics, 2019, 155-165.

    Indig Balázs, Sass Bálint, Simon Eszter, Mittelholcz Iván, Kundráth Péter, Vadász Noémi. emtsv – Egy formátum mind felett. In: Berend Gábor, Gosztolya Gábor, Vincze Veronika (szerk.): MSZNY 2019, XV. Magyar Számítógépes Nyelvészeti Konferencia (MSZNY 2019). Szeged: Szegedi Tudományegyetem Informatikai Tanszékcsoport, 235-247.

    Váradi Tamás, Simon Eszter, Sass Bálint, Mittelholcz Iván, Novák Attila, Indig Balázs: e-magyar – A Digital Language Processing System. In: Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018), 1307-1312.

    Váradi Tamás, Simon Eszter, Sass Bálint, Gerőcs Mátyás, Mittelholcz Iván, Novák Attila, Indig Balázs, Prószéky Gábor, Farkas Richárd, Vincze Veronika: Az e-magyar digitális nyelvfeldolgozó rendszer. In: MSZNY 2017, XIII. Magyar Számítógépes Nyelvészeti Konferencia, Szeged: Szegedi Tudományegyetem Informatikai Tanszékcsoport, 49-60.

If you use [__emMorph__](https://github.com/nytud/emMorph) module, please cite:

    Attila Novák, Borbála Siklósi, Csaba Oravecz: A New Integrated Open-source Morphological Analyzer for Hungarian. In: Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC 2016), Paris: European Language Resources Association (ELRA).
 
    Attila Novák: A New Form of Humor -- Mapping Constraint-Based Computational Morphologies to a Finite-State Representation. In: Proceedings of the Ninth International Conference on Language Resources and Evaluation (LREC 2014), Paris: European Language Resources Association (ELRA).
   
If you use [__emTag__ (PurePos)](https://github.com/ppke-nlpg/purepos) module, please cite:

    Orosz György, Novák Attila: PurePos 2.0: a hybrid tool for morphological disambiguation. In: Proceedings of the International Conference on Recent Advances in Natural Language Processing (RANLP 2013), 539-545.

If you use __emBERT__ module, please cite:

    Nemeskey Dávid Márk: Egy emBERT próbáló feladat. In: MSZNY 2020, XVI. Magyar Számítógépes Nyelvészeti Konferencia. Szeged: Szegedi Tudományegyetem Informatikai Tanszékcsoport, 409-418.

If you use __emPreverb__ or __emCompound__ module, please cite:

    Pethő Gergely, Sass Bálint, Kalivoda Ágnes, Simon László, Lipp Veronika: Igekötő-kapcsolás. In: MSZNY 2022, XVIII. Magyar Számítógépes Nyelvészeti Konferencia. Szeged: Szegedi Tudományegyetem Informatikai Intézet, 77-91.
 
The __emtsv__ system is a replacement for the original https://github.com/nytud/hunlp-GATE system.

__emtsv__ is licensed under [LGPL 3.0](LICENSE). The submodules have their own licenses.

## Requirements

- GIT LFS (see notes)
- Python 3.5 <=
- HFST 3.13 <=
- Hunspell (libhunspell-dev, hunspell-hu) 1.6.2 <=
- OpenJDK 11 JDK (not JRE)
- An UTF-8 locale must be set.

## Installation

- From the git repository: see [detailed instructions](docs/installation.md) in the documentation
- From __prebuilt docker image__ ([https://hub.docker.com/r/mtaril/emtsv](https://hub.docker.com/r/mtaril/emtsv)):
    ```bash
    docker pull mtaril/emtsv:latest
    ```
    - See [detailed instructions](docs/installation.md) for building the _docker image_

## Usage

Here we present the usage scenarios. [The individual modules are documented in detail below.](#modules)
<br/>
To extend the toolchain with new modules [just add new modules to `config.py`](#creating-a-module).

### Command-line interface

- Multiple modules at once (not necessarily starting with raw text):
    ```bash
    echo "A kutya elment sétálni." | python3 ./main.py tok,spell,morph,pos,conv-morph,dep,chunk,ner
    ```
- Modules _glued together_ one by one with the _standard *nix pipelines_ __where users can interact with the data__ between the modules:
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
- Independently from the other options, `emtsv` can also be used with input or output streams redirected or with string input (this applies to the runnable docker form as well):
    ```bash
    python3 ./main.py tok,spell,morph,pos,conv-morph,dep,chunk,ner -i input.txt -o output.txt
    python3 ./main.py tok,spell,morph,pos,conv-morph,dep,chunk,ner --text "A kutya elment sétálni."
    ```

### Docker image

#### Runnable docker form (CLI usage of docker image):
    ```bash
    cat input.txt | docker run -i mtaril/emtsv tok,morph,pos > output.txt
    ```
#### As service through Rest API (docker container)
```bash
docker run --rm -p5000:5000 -it mtaril/emtsv  # REST API listening on http://0.0.0.0:5000
```
The container starts two emtsv processes by default. Should the throughput
be insufficient (or conversely, the memory requirements too great even
with two processes), this number can be configured via the
`EMTSV_NUM_PROCESSES` variable:
```bash
docker run --rm -p5000:5000 -it -e "EMTSV_NUM_PROCESSES=4" mtaril/emtsv
```

### REST API

#### Server:
- __RECOMMENDED WAY__: Docker image ([see above](#as-service-through-rest-api-docker-container))
- Any wsgi server (`uwsgi`, `gunicorn`, `waitress`, etc.) can be configured to run with [docker/emtsvREST.wsgi](docker/emtsvREST.wsgi) .
- Debug server (Flask) __only for development (single threaded, one request at a time)__:
    ```bash
    # Without parameters!
    python3 ./main.py
    ```
    When the server outputs a message like `* Running on` then it is ready to accept requests on http://127.0.0.1:5000 .
    (__We do not recommend using this method in production as it is built atop of Flask debug server! Please consider using the Docker image for REST API in production!__)



#### Client:
- Web frontend provided by `xtsv` (without any URL parameters)
- From Python:
    ```python
    >>> import requests
    >>> # With input file
    >>> # The URL contains the tools to be run separated by `/` instead of ',' used in the CLI
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
    The server checks whether the module order with the provided input data is feasible, and returns an error message if there are any problems.
- By `curl`:
   ```bash
   echo "A kutya elment sétálni." | curl -F "file=@-" http://SERVER:PORT/tok/morph/pos
   ```
### As Python Library

1. Install emtsv in `emtsv` directory or make sure the emtsv installation is in the `PYTHONPATH` environment variable
2. `import emtsv`
3. Now the full API is accessible (see the example above):
    ```python
    import sys
    from emtsv import build_pipeline, jnius_config, tools, presets, process, pipeline_rest_api, singleton_store_factory

    jnius_config.classpath_show_warning = False  # To suppress warning

    # Imports end here. Must do only once per Python session

    # Set input from any stream or iterable and output stream...
    input_data = sys.stdin
    output_iterator = sys.stdout
    # Raw, or processed TSV input list and output file...
    # input_data = iter(['A kutya', 'elment sétálni.'])  # Raw text line by line
    # Processed data: header and the token POS-tag pairs line by line
    # input_data = iter([['form', 'xpostag'], ['A', '[/Det|Art.Def]'], ['kutya', '[/N][Nom]'], ['elment', '[/V][Pst.NDef.3Sg]'], ['sétálni', '[/V][Inf]'], ['.', '.']])
    # output_iterator = open('output.txt', 'w', encoding='UTF-8')  # File
    # input_data = 'A kutya elment sétálni.'  # Or raw string in any acceptable format.

    # Select a predefined task to do or provide your own list of pipeline elements
    used_tools = ['tok', 'morph', 'pos']

    conll_comments = True  # Enable the usage of CoNLL comments

    # Run the pipeline on input and write result to the output...
    output_iterator.writelines(build_pipeline(input_data, used_tools, tools, presets, conll_comments))

    # Alternative: Run specific tool for input streams (still in emtsv format).
    # Useful for training a module (see Huntag3 for details):
    output_iterator.writelines(process(sys.stdin, an_inited_tool))

    # Or process individual tokens further... WARNING: The header will be the first item in the iterator!
    for tok in build_pipeline(input_data, used_tools, tools, presets, conll_comments):
        if len(tok) > 1:  # Empty line (='\n') means end of sentence
            form, xpostag, *rest = tok.strip().split('\t')  # Split to the expected columns

    # Alternative2: Flask application (REST API)
    singleton_store = singleton_store_factory()
    app = application = pipeline_rest_api(name='e-magyar-tsv', available_tools=tools, presets=presets,
                                conll_comments=conll_comments, singleton_store=singleton_store,
                                form_title='e-magyar text processing system',
                                doc_link='https://github.com/nytud/emtsv')
    # And run the Flask debug server separately
    app.run()
    ```

The public API is equivalent to the [`xtsv` API](https://github.com/nytud/xtsv#api-documentation)

## Data format

Please see the specification  in detail in the [`xtsv` documentation](https://github.com/nytud/xtsv#data-format).

For examples see files in `tests/test_input` and `tests/test_output` directories.

## Modules

Modules are defined in `config.py`. The current toolchain consists of the following modules which can be called by their names (or using their shorthand names in brackets):

- `emToken` (`tok`): Tokenizer
- `emMorph` (`morph`): Morphological analyser together with emLem lemmatiser
- `hunspell` (`spell`): Spellchecker, stemmer and morphological analyser
- `emTag` (`pos`): POS-tagger
- `emChunk` (`chunk`): Maximal NP-chunker
- `emNER` (`ner`): Named-entity recogniser
- `emmorph2ud` (`conv-morph`): Converter from emMorph code to UDv1 _upos_ and _feats_ format
- `emmorph2ud2` (`conv-morph2`): Converter from emMorph code to UDv2 _upos_ and _feats_ format
- `emDep-ud` (`dep`): Dependency parser
- `emDep-ud50` (`dep50`): Dependency parser
- `emCons` (`cons`): Constituent parser
- `emCoNLL` (`conll`): Converter from emtsv to CoNLL-U format
- `emDummy` (`dummy-tagger`): Example module
- `udpipe-tok`: The UDPipe tokeniser
- `udpipe-pos`: The UDPipe POS-tagger
- `udpipe-parse`: The UDPipe depenceny parser
- `udpipe-pos-parse`: From POS-tagging to dependency parsing in __'one step'__ with UDPipe, roughly (!) the same as `udpipe-pos,udpipe-parse`
- `udpipe-tok-parse`: From tokenisation to dependency parsing in __'one step'__ with UDPipe, roughly (!) the same as `udpipe-tok,udpipe-pos,udpipe-parse`
- `udpipe-tok-pos`: From tokenisation to POS-tagging in __'one step'__ with UDPipe, roughly (!) the same as `udpipe-tok,udpipe-pos`
- `emTerm` (`term`): a module for marking single word and multi-word units in POS-tagged text
- `emZero` (`zero`): a module for inserting zero pronouns (subjects, objects and possessors) into dependency parsed sentences
- `emBERT-NER` (`bert-ner`): module that wraps NER model based on huBERT
- `emBERT-baseNP` (`bert-basenp`): module that wraps base NP chunker based on huBERT 
- `emBERT-NP` (`bert-np`, `bert-chunk`): module that wraps maximal NP chunker based on huBERT 
- `emIOBUtils-NP` (`fix-np`, `fix-chunk`): a module for converting among IOB representations and fixing invalid label sequences the present one
- `emIOBUtils-NER` (`fix-ner`, `fix-ner`): a module for converting among IOB representations and fixing invalid label sequences the present one
- `emGATEConv` (`gate-conv`): a module for converting the output TSV format to GATE XML. The purpose of the module is to help the transition of http://e-magyar.hu form GATE to emtsv, therefore only the minimal required featureset is implemented
- `emStanza-tok` (`emstanza-tok`, `stanza-tok`): The Stanza tokeniser
- `emStanza-pos` (`emstanza-pos`, `stanza-pos`): The Stanza POS tagger (no lemmatisation)
- `emStanza-lem` (`emstanza-lem`, `stanza-lem`): The Stanza POS tagger including lemmatisation
- `emStanza-parse` (`emstanza-parse`, `stanza-parse`, `emStanza-dep`, `emstanza-dep`, `stanza-dep`): The Stanza dependency parser
- `emStanza-tok-lem` (`emstanza-tok-lem`, `stanza-tok-lem`): The Stanza tokeniser, POS tagger and lemmatiser as a whole
- `emStanza-tok-parse` (`emstanza-tok-parse`, `stanza-tok-parse`, `emStanza-tok-dep`, `emstanza-tok-dep`, `stanza-tok-dep`): The Stanza tokenizer, POS tagger, lemmatiser and dependency parser as a whole
- `emPhon-IPA-comments` (`emphon-ipa-comments`, `emPhon-ipa-comments`): The emPhon phonetic transcriber with IPAization and with comment lines
- `emPhon-IPA-nocomments` (`emphon-ipa-nocomments`, `emPhon-ipa-nocomments`): The emPhon phonetic transcriber with IPAization but without comment lines
- `emPhon-noIPA-comments` (`emphon-noipa-comments`, `emPhon-noipa-comments`): The emPhon phonetic transcriber without IPAization but with comment lines
- `emPhon-noIPA-nocomments` (`emphon-noipa-nocomments`, `emPhon-noipa-nocomments`): The emPhon phonetic transcriber without IPAization and comment lines
- `emPreverb` (`preverb`): module to connect a preverb to the verb or verb-derivative token to which it belong.
- `emCompound` (`compound`): module to annotate compound boundaries.

For an overview see [the topology of the current toolchain](docs/emtsv_modules.pdf)

The following presets are defined as shorthands for the common tasks:

- `analyze`: Run the full pipeline, same as: `emToken,emMorph,emTag,emChunk,emNER,emmorph2ud,emDep-ud,emCons`
- `tok-morph`: From tokenisation to morphological analysis, same as `emToken,emMorph`
- `tok-pos`: From tokenisation to POS-tagging, same as `emToken,emMorph,emTag`
- `tok-chunk`: From tokenisation to maximal NP-chunking, same as `emToken,emMorph,emTag,emChunk`
- `tok-ner`: From tokenisation to named-entity recognition, same as `emToken,emMorph,emTag,emNER`
- `tok-udpos`: From tokenisation to POS-tagging in UD format, same as `emToken,emMorph,emTag,emmorph2ud`
- `tok-dep`: From tokenisation to dependency parsing, same as `emToken,emMorph,emTag,emmorph2ud,emDep-ud`
- `tok-bert-ner`: Raw text to emBERT named-entity annotation, same as `emToken,emBERT-NER`
- `tok-bert-chunk`: Raw text to emBERT maximal NP chunking, same as `emToken,emBERT-NP`

### Example

[The examples presented above](#command-line-interface) simply call `main.py` with the parameters `tok,spell,morph,pos,conv-morph,dep,chunk,ner` take the input on STDIN and return the output on STDOUT.
We use here a tokenizer, a morphological analyzer, a POS tagger, a morphology converter, a dependency parser, a chunker and a named entity recognizer.
(The converter is needed as the POS tagger and the dependency parser work with different morphological coding systems.)

### Creating a module

- The method is the same as in the case of [creating modules in `xtsv`](https://github.com/nytud/xtsv#creating-a-module-that-can-be-used-with-xtsv)
- However, all new modules must follow [the field-name conventions of `emtsv`](docs/emtsv_modules.pdf)

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

- [installation](docs/installation.md)
- [testing](docs/testing.md)
- [troubleshooting](docs/troubleshooting.md)
