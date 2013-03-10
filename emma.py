
import socket
import urllib
import urllib2
import time
import subprocess
import re
import textwrap
import random
import json

def get_line():
    try: f = open('temp','r')
    except: return
    line = f.read()
    f.close()
    return line

def f_write(name,content,method):
    f = open (name,method)
    f.write(content)
    f.close()

def get_header(input):
    print '--- Begin header function ---\n'

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/5.0')]
    try:
        html = opener.open(input).read()
    except urllib2.HTTPError, e:
        return 'Error: ' + str(e) + '.'
    try: title = '\x02Title: \x02' + html.split('title>')[1].split('</')[0]
    except: title = '\x02Title: \x02unresolvable'
    print 'Determined <title> - ' + title
    print '\n--- End header function ---\n'

    return title

def check_twitter(user,type):
    print '--- Begin twitter function ---\n'

    output = []
  
    request = 'https://api.twitter.com/1/statuses/user_timeline.json?include_entities=true&include_rts=true&screen_name=' + user + '&count=1'
    print 'Opening - ' + request
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/5.0')]
    try:
        data = opener.open(request).read()
    except urllib2.HTTPError, e:
        return ['Error: ' + str(e) + '.']
    print '--> Opened\n'
    if data == []:
        return ['Error.']
    data = json.loads(data)[0]   
    if type == 'add' or type == 'del':
        f = open('twitter.users','r')
        users = f.read().splitlines()
        f.close()
        for existing in users:
            if user == existing:
                print 'Found ' + user + 'in twitter.users.'
                if type == 'add':
                    print 'Did not add ' + user + ' to twitter.users; user already exists.'
                    output.append('I am already following ' + user + '\'s tweets.')
                    return output
                if type == 'del':
                    print 'Deleted ' + user + ' from twitter.users.'
                    for existing in users:
                        if existing != user:
                            f_write('twitter.users',existing+'\n','w')
                            output.append('Deleted \x02' + user + '\x02from file; no longer following \x02' + user + '\x02.')
                            return output
        f_write('twitter.users',user+'\n','a')
        print 'Added ' + user + ' to file.'    
        output.append('\x02' + user + ' \x02has been successfully added.')

    try:
        time = data['created_at'].split(' +')[0]
        tweet = data['text']
        output.append('\x02Last tweet\x02 --- ' + '\x02' + time + '\x02 --- \x02' + tweet + '\x02')
        print '\n--- End twitter function ---\n'
        return output
    except:
        output.append('Twitter screen name does not exist.')
        print '\n--- End twitter function ---\n'
        return output    

def get_quote(input):
    print '--- Begin quote function ---\n'    
    
    input = input.split('!quote ')[1].strip()
    try: input = input.replace(' ','_')
    except: pass
    url = 'http://www.goodreads.com/search?utf8=%E2%9C%93&q='+input.title()
    url = url +'&search_type=books&search%5Bfield%5D=author'
    print 'Opening - ' + url
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/5.0')]
    html = opener.open(url).read()
    try:
        url = html.split('hema.org/Person\'>')[1].split('\" class=\"authorName')[0].split('href=\"')[1]
    except:
        return 'Error: Unable to find author on goodreads.com'
    id = url.split('show/')[1]
    print '--> Author ID - ' + id
    url = 'http://www.goodreads.com/author/quotes/' + id
    print '  --> New URL - ' + url
    html = opener.open(url).read()
    print '\nOpening - ' + url
    quotes = [] 

    for i in range(10):
        try: 
            quotes.append(str(html.split('&ldquo;')[1].split('&rdquo;')[0]))
            try: quotes[i] = quotes[i].replace('<br />',' ')
            except: raise
            html = html.partition('&#8213;')[2]
            print '\nAdded quote #' + str(i+1)
        except:
            pass

    num = random.randint(0,9)
    quote = quotes[num]
    
    print '\n Quote: ' + quote

    print '\n--- End quote function ---\n'

    return quote
    
def get_whois(input):
    print '--- Begin whois function ---\n'
    print '\nraw input: ' + input
    arg = input.split('!whois ')[1].strip()
    print 'user argument: ' + arg
    try:
        if re.match("\d+\.\d+\.\d+\.\d+",arg):
            ip = arg
            print '\n Determined IP - ' + ip + ' - from user'
        else:
            data = subprocess.Popen(['./dig',arg],stdout=subprocess.PIPE).stdout.read()
            ip = data.split('ANSWER SECTION')[1].split(arg)[1].split('A')[1].split('\n')[0].strip()
            print '\n Determined IP - ' + ip + ' - using dig'
        data = urllib.urlopen('http://whatismyipaddress.com/ip/'+ip).read()
        country = data.split('Country:</th><td>')[1].split('<')[0].strip()
	print '\n Determined country - ' + country
        try:
            region = data.split('State/Region:</th><td>')[1].split('<')[0]
            city = data.split('City:</th><td>')[1].split('<')[0]
        except:
            region = '<unknown>'
            city = region
	print '\nDetermined city and region - ' + city + ', ' + region
        isp = data.split('ISP:</th><td>')[1].split('<')[0]
        print '\nDetermined ISP - ' + isp
	org = data.split('Organization:</th><td>')[1].split('<')[0]
        print '\nDetermined organization - ' + org
	data = subprocess.Popen(['./dig','-x',ip],stdout=subprocess.PIPE).stdout.read()
        try: host = data.split('ANSWER SECTION')[1].split('PTR')[1].split('\n')[0].strip().strip('.')
        except: pass
        output = '\x02IP Details for \x02' + ip
        output = output + '\n\n\x02Location: \x02' + city + ', ' + region + ', ' + country
        try: output = output + '\n\x02Host: \x02' + host
        except: output = output + '\n\x02Host:\x02 \x034unresolvable'
        output = output + '\n\x02ISP: \x02' + isp
        output = output + '\n\x02Organization: \x02' + org
        print '\nProcess complete'
	print '\n\nOutput: \n\n' + output
        print '\n--- End whois function ---\n'
	return output.splitlines()
    except:
        return 'Error'

def get_wiki(input):
    input = input.split('!wiki ')[1]
    if input.splitlines():
        input = input.replace(' ','_').title()
    print '--- Begin wiki function ---\n\nSearching for: ' + input
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/5.0')]
    try:
        url = 'http://en.wikipedia.org/wiki/'+input
        print '\nOpening - ' + url
	html = opener.open(url).read()
        print '--> Opened'
        title = html.split('title>')[1].split(' -')[0]
        print '\nTitle - ' + title
        content = html.split('<p>')[1].split('</p>')[0]
        content = re.sub(r'<.*?>','',content)
        content = re.sub(r'\[.*?\]','',content)
        print '\nContent: \n' + content
        if len(content) < 50:
            others = html.split('</p>\n<ul>')[1].split('</ul>')[0]
            others = re.sub(r'<.*?>','',others)
        content = textwrap.fill(content,75)
        output = '\x031,0Wikipedia\x03 article on ' + title
        output = output + '\n----------------------------------------------------------------\n' + content
        try:
            others
            output = output + others
        except: pass
        print '\n--- End wiki function ---\n'
        return output.splitlines()
    except urllib2.HTTPError, e:
        print str(e)


print """

-----------------------------
Emma - Python IRC Bot - v 0.2
-----------------------------

"""


network = 'localhost'
port = 60000
auth = 'emma:thetreeisminute'

irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
print 'Established connection with ' + network + ':' + str(port)

irc.send ( 'NICK emma\r\n' )
print '\n\nSent NICK'

irc.send ( 'USER emma emma emma :em ma\r\n' )
print 'Sent USER'

irc.send ( 'PASS ' + auth + '\r\n' )
print 'Sent PASS\n'

while 1:

    # Handles PING/PONGS
    data = irc.recv ( 4096 )
    if data.find ( 'PING' ) != -1:
        irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )

    # Handles http headers
    if data.find ( 'http://' ) != -1 and data.find ( 'https://' ) and data.find ( 'poemhunter.com/' ) == -1:
        url = data.split(':',1)[1].split(':',1)[1].partition('http')
        url = url[1] + url[2]
        try: 
            url = url.split(' ')[0]
        except:
            pass
        irc.send ( 'PRIVMSG #talk :' + get_header(url) + '\r\n' )

    # Handles poemhunter.com requests
    if data.find ( 'http://www.poemhunter.com/poem/' ) != -1:
        url = data.split(':',1)[1].split(':',1)[1].partition('http://')
        url = url[1] + url[2]
        try:
            url = url.split(' ')[0]
        except:
            pass
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent','Mozilla/5.0')]
        html = opener.open(url).read()
        title = html.split('<h2 ')[1].split('</h2')[0].split('>')[1]
        author = html.split('author\">')[1].split('</div>')[0]
        contents = html.split('KonaBody\">')[1].split('</p>')[0].split('<p>')[1].split('<br />')
        del contents[-1]
        irc.send ( 'PRIVMSG #talk :\x02' + title + '\x02 by \x02' + author + '\x02\r\n' )
        print title + ' by ' + author
        for line in contents:
            line = line.strip()
            irc.send ( 'PRIVMSG #talk :' + line + '\r\n' )
            print line
            time.sleep(0.5)

    # Handles !twitter requests
    if data.find ( '!twitter ' ) != -1:
        message = data.split(' :')[1].split()
        if len(message) == 2:
            for line in check_twitter(message[1],''):
                irc.send ( 'PRIVMSG #talk :' + line.encode('utf-8') + '\r\n' )
        if len(message) == 3 and (message[1] == 'add' or message[1] == 'del'):
            for line in check_twitter(message[2],message[1]): 
                irc.send ( 'PRIVMSG #talk :' + line.encode('utf-8') + '\r\n' )
        if len(message) == 2 and message [1] == 'help':
            irc.send ( 'PRIVMSG #talk :I do live tweets. Usage - !twitter add <username>.\r\n' )
        
                
    # Handles !wiki requests
    if data.find ( '!wiki' ) != -1:
        for line in get_wiki(data):
            irc.send ( 'PRIVMSG #talk :' + line + '\r\n' )
            time.sleep(0.5)

    # Handles !quote requests
    if data.find ( ':!quote ' ) != -1:
        args = len(data.split('!quote ')[1].split())
        if args > 0 and args < 5:
            irc.send ( 'PRIVMSG #talk :' + get_quote(data) + '\r\n' )
        else:
            irc.send ( 'PRIVMSG #talk : Try again; correct syntax is !author first (middle) last\r\n' )
        
    # Handles !whois requests
    if data.find ( '!whois' ) != -1:
        for line in get_whois(data):
            irc.send ( 'PRIVMSG #talk :' + line + '\r\n' )
            time.sleep(0.5)
   
    # Handles passive messaging from username 'geddes'
    if data.find ( ':geddes!geddes@local.host PRIVMSG emma :' ) != -1:
        message = data.split(' :')[1]           
        irc.send ( 'PRIVMSG #talk :' + message + '\r\n' )

    # Handles NOTICE on JOIN
    if data.find ( 'JOIN :#talk' ) != -1 and data.find ( 'emma' ) == -1:
        print '\nNew JOIN \n --> ' + data
        nick = data.split(':')[1].split('!')[0] 
        print '\n  --> ' + nick
        irc.send ( 'NOTICE ' + nick + ' :Welcome to #talk. I come with !wiki <term> and !whois <ip/domain> functions. Play nice.\r\n' )

