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
  File "./emMorphREST.py", line 25, in <module>
    app.run(debug=True)
  File "/home/joker/tmp/emTSV-virtual/lib/python3.5/site-packages/flask/app.py", line 943, in run
    run_simple(host, port, self, **options)
  File "/home/joker/tmp/emTSV-virtual/lib/python3.5/site-packages/werkzeug/serving.py", line 795, in run_simple
    s.bind(get_sockaddr(hostname, port, address_family))
OSError: [Errno 98] Address already in use
```

Input: tokenized sentences separated by newlines (`\n`).
What could be this one? :)

