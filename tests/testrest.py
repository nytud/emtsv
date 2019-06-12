import sys
import requests
r = requests.post('http://127.0.0.1:5000/' + sys.argv[1], files={'file': open(sys.argv[2], encoding='UTF-8')})
print(r.text, end='') 

