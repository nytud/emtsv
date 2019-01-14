import requests
#r = requests.post('http://juniper.nytud.hu:5000/tok/morph/pos', files={'file':open('test_input/input.test', encoding='UTF-8')})
r = requests.post('http://127.0.0.1:5000/tok/morph/pos', files={'file':open('test_input/input.test', encoding='UTF-8')})
print(r.text)
