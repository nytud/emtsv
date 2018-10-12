# emTSV
TSV style format and REST API for e-magyar implemented in Python

This is a quick and dirty RFC implementation. Bugs can happen!

Please leave feedback!

## Usage

	```python
	>>> import requests
	>>> r = requests.post('http://127.0.0.1:5000/command', files={'file':open('test.text', encoding='UTF-8')})
	>>> print(r.text)
	...
	```
