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

`pip install -r emmorphpy/requirements.txt`

`pip install -r purepospy/requirements.txt`

`pip install -r emdeppy/requirements.txt`

`pip install -r HunTag3/requirements.txt`

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

