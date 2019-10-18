# Testing

## Command-line interface

To automatically check that everything is ok with the command-line interface, simply run:

```bash
./tests/test.sh
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
`make test-tok-morph-tag` runs the modules separately,
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
./tests/testrest.sh
```
