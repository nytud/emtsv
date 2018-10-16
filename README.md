# emTSV
TSV style format and REST API for e-magyar implemented in Python

This is a quick and dirty RFC implementation. Bugs can happen!

Please leave feedback!

## Requirements

python 3.5 <=

## Install

`git clone --recurse-submodules https://github.com/dlazesz/emTSV`

## Usage

```
  python
	>>> import requests
	>>> r = requests.post('http://127.0.0.1:5000/command', files={'file':open('test.text', encoding='UTF-8')})
	>>> print(r.text)
	...
```

# testing :)

`Makefile` created for testing purposes.

First results:

`make test-chunk-chain`

```
cat test_input/input.test | sed "s/\([.,;:?!]\)/ \1/" | tr ' ' '\n' | python3 ./emMorphREST.py --pipe
Traceback (most recent call last):
  File "./emMorphREST.py", line 11, in <module>
    from emmorphpy import EmMorphPy
  File "./emmorphpy/emmorphpy/__init__.py", line 1, in <module>
    from .emmorphpy import EmMorphPy
  File "./emmorphpy/emmorphpy/emmorphpy.py", line 461
    self.p = subprocess.Popen([hfst_lookup, *params, fsa], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                       ^
SyntaxError: can use starred expression only as assignment target
/home/joker/Makefile.emTSV:8: recipe for target 'test-chunk-chain' failed
make: *** [test-chunk-chain] Error 1
```

`make test-tag-only`

```
cat test_input/emTag.test | python3 ./emTagREST.py --pipe
string  anas  lemma hfstana
WARNING: No blank line before EOF!
Compiling model...Traceback (most recent call last):
  File "./emTagREST.py", line 23, in <module>
    sys.stdout.writelines(process(sys.stdin, em_tag))
  File "/home/joker/tmp/emTSV/TSVRESTTools/tsvhandler.py", line 37, in process
    yield from ('{0}\n'.format('\t'.join(tok)) for tok in internal_app.process_sentence(sen, field_values))
  File "./purepospy/purepospy.py", line 197, in process_sentence
    for tok, tagged in zip(sen, self.tag_sentence(' '.join(sent)).split()):
  File "./purepospy/purepospy.py", line 130, in tag_sentence
    read_mod = serializer().readModel(self._model_jfile)
  File "jnius/jnius_export_class.pxi", line 637, in jnius.JavaMethod.__call__
  File "jnius/jnius_export_class.pxi", line 803, in jnius.JavaMethod.call_staticmethod
  File "jnius/jnius_utils.pxi", line 93, in jnius.check_exception
jnius.JavaException: JVM exception occurred: äí (No such file or directory)
Makefile:23: recipe for target 'test-tag-only' failed
make: *** [test-tag-only] Error 1
```

`make test-dep-only`

```
cat test_input/emDep.test | python3 ./emDepREST.py --pipe
49.36.423  is2.parser.Parser -1:readModel ->           Reading data started
java.io.EOFException
  at java.io.DataInputStream.readInt(DataInputStream.java:392)
  at is2.parser.MFO.read(Unknown Source)
  at is2.parser.Parser.readModel(Unknown Source)
  at is2.parser.Parser.<init>(Unknown Source)
  at is2.parser.Parser.<init>(Unknown Source)
string  lemma pos feature deptype deptarget
WARNING: No blank line before EOF!
java.lang.NullPointerException
  at is2.parser.Parser.parse(Unknown Source)
  at is2.parser.Parser.apply(Unknown Source)
Traceback (most recent call last):
  File "./emDepREST.py", line 23, in <module>
    sys.stdout.writelines(process(sys.stdin, em_dep))
  File "/home/joker/tmp/emTSV/TSVRESTTools/tsvhandler.py", line 37, in process
    yield from ('{0}\n'.format('\t'.join(tok)) for tok in internal_app.process_sentence(sen, field_values))
  File "./emdeppy/emdeppy/emdeppy.py", line 32, in process_sentence
    tok[field_names[3]])) for tok in sen)
  File "./emdeppy/emdeppy/emdeppy.py", line 69, in parse_sentence
    return zip(count(start=1), out.forms, out.plemmas, out.ppos, out.pfeats, out.pheads, out.plabels)
AttributeError: 'NoneType' object has no attribute 'forms'
Makefile:27: recipe for target 'test-dep-only' failed
make: *** [test-dep-only] Error 1
```

What went wrong? :)

