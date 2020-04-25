from services import TwitterService
from json import dumps

ts = TwitterService()
x = 0
for t in ts.list_my_tweets():
    print(t.text)
    x += 1

print(x)
