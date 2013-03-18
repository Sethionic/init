#!/usr/bin/env python
import cgi,os,sys,getpass,cgitb,Cookie,sha,time,MySQLdb
import session as ss
form = cgi.FieldStorage()
sss=ss.Session()

DBServer='127.0.0.1'
DBUser=''
DBPass=''
DBName=''
db = MySQLdb.connection(host=DBServer,user=DBUser,passwd=DBPass,db=DBName)
DB = db.query

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


#cookie = Cookie.SimpleCookie()
#string_cookie = os.environ.get('HTTP_COOKIE')
# If new session
#if not string_cookie:
   # The sid will be a hash of the server time
#   sid = sha.new(repr(time.time())).hexdigest()
   # Set the sid in the cookie
#   cookie['sid'] = sid
   # Will expire in a year
#   cookie['sid']['expires'] = 60 * 60 #12 * 30 * 24 * 
# If already existent session
#else:
#   cookie.load(string_cookie)
#   sid = cookie['sid'].value

#print cookie

#Figure out who is requesting the page
User=getpass.getuser()
if User=='root':
    ClientIP='127.0.0.1'
elif User=='www-data':
    ClientIP=cgi.escape(os.environ["REMOTE_ADDR"])
cgitb.enable()

#See if a user submitted content
if sss.loggedIn() & ("messages" in form):
    try:
        data=cgi.escape(strip_tags(form.getvalue('usermessage')))
        DB("INSERT INTO QPosts (Quser,Qmessage) VALUES ('{0}','{1}')".format(sss.getUser(),data))
        form=1
    except:
        DB("INSERT INTO QPosts (Quser,Qmessage) VALUES ('{0}','{1}')".format(sss.getUser(),"Something Malicious... tsk tsk..."))
        form=0


#Fetch the recent posts
db.query("SELECT * FROM QPosts order by Qtime desc limit 10")
r = db.store_result()

#Enumerate results
history = ""
for row in r.fetch_row(10):
    history += cgi.escape(row[1])+" said at " + cgi.escape(row[3]) +":<br>"+ cgi.escape(row[2]) + "<br><br>\n"
    
try:
    print "Content-Type: text/html"
    print 

    print """
    <html><head><title>Message Board</title></head>
<body><h1>Message Board</h1>
Recent Posts<hr>
<b>What do users have to say?: </b><br>
"""
    print history
    if sss.getUser()<>'Anonymous User': print """
<hr>
<form method=POST>Have anything to say?: <br><textarea name="usermessage" cols="40" rows="4">This is awesome!</textarea><br>
<input type=submit name="messages" value="Comment">
</form>
"""
    print "<hr>Currently viewing as: {0}".format(sss.getUser())
    print "<br><a href='auth.py?x=R'>Register</a> <a href='auth.py?x=L'>Login</a> <a href='auth.py?x=F'>Forgot Password?</a>"
    print "</body></html>"


except:
    #Errors only printed for localhost
    if ClientIP<>'127.0.0.1':
        print """\
<html><body>
Whoa there
</body></html>
"""