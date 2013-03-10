import json
from pprint import pprint
import urllib2

s_n = 'astronnash'
request = 'https://api.twitter.com/1/statuses/user_timeline.json?include_entities=true&include_rts=true&screen_name=' + s_n + '&count=1'

opener = urllib2.build_opener()
opener.addheaders = [('User-agent','Mozilla/5.0')]
data = opener.open(request).read()

data = json.loads(data)[0]

pprint(data)

print data['created_at'].split(' +')[0] + ' ' + data['text']

f = open('twitter.users','r')
users = f.read().splitlines()
f.close()

user = 'asdf'

for existing in users:
    if user == existing:
        print 'I am already watching ' + user + '\'s tweets.'

