import requests
import json

shortcode = "CRmMGUlnbNb"

head = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
req_link = f"https://www.instagram.com/graphql/query/?query_hash=a9441f24ac73000fa17fe6e6da11d59d&variables=%7B%22shortcode%22%3A%22{shortcode}%22%7D"
print(req_link)
r = requests.get(req_link, headers = head)
# json_data = json.loads(r.content)

print(r.content)