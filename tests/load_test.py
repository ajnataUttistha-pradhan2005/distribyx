import requests
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:8080/load"

def hit():
    try:
        r = requests.get(URL)
        print(r.status_code)
    except:
        print("fail")

with ThreadPoolExecutor(max_workers=50) as executor:
    for _ in range(1000):
        executor.submit(hit)