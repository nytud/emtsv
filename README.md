# emTSV
TSV style format and REST API for e-magyar implemented in Python

This is a quick and dirty RFC implementation. Bugs can happen!

Please leave feedback!

## Requirements

python 3.5 <=

## Install

Clone together with submodules:

`git clone --recurse-submodules https://github.com/dlazesz/emTSV`

`pip3 install Cython` (for emdeppy, must be installed in a separate step)

Then install requirements for submodules:

`pip3 install -r emmorphpy/requirements.txt`

`pip3 install -r purepospy/requirements.txt`

`pip3 install -r emdeppy/requirements.txt`

`pip3 install -r HunTag3/requirements.txt`

## Usage

```
  python
	>>> import requests
	>>> r = requests.post('http://127.0.0.1:5000/command', files={'file':open('test.text', encoding='UTF-8')})
	>>> print(r.text)
	...
```

## Testing

`make test-morph-tag INPUT=test_input/puzser.test`

Morphological analysis (emMorph+emLem) + POS tagging (emTag=purepos) works! :)

-----

`./mnsz2_test.sh`

```
Traceback (most recent call last):
  File "./emTagREST.py", line 23, in <module>
    sys.stdout.writelines(process(sys.stdin, em_tag))
  File "/home/joker/tmp/emTSV-virtual/emTSV/TSVRESTTools/tsvhandler.py", line 37, in process
    yield from ('{0}\n'.format('\t'.join(tok)) for tok in internal_app.process_sentence(sen, field_values))
  File "./purepospy/purepospy.py", line 196, in process_sentence
    m.anals[token] = self._add_ana_if_any(tok[field_indices[1]])
IndexError: list index out of range
Traceback (most recent call last):
  File "./emMorphREST.py", line 23, in <module>
    sys.stdout.writelines(process(sys.stdin, em_morph))
BrokenPipeError: [Errno 32] Broken pipe
```

Input: tokenized sentences separated by newlines (`\n`).
What could be this one? :)

