#!/usr/bin/env python
import cgi,os,sys,getpass,cgitb,Cookie,sha,time,MySQLdb,smtplib,random,string
import session as ss
from email.mime.text import MIMEText
from threading import Thread
form = cgi.FieldStorage()
sss=ss.Session()


DBServer='127.0.0.1'
DBUser=''
DBPass=''
DBName=''
db = MySQLdb.connection(host=DBServer,user=DBUser,passwd=DBPass,db=DBName)
DB = db.query

#Figure out who is requesting the page
User=getpass.getuser()
if User=='root':
    ClientIP='127.0.0.1'
elif User=='www-data':
    ClientIP=cgi.escape(os.environ["REMOTE_ADDR"])
cgitb.enable()

class Auth:
    def __init__(self,mode='Null'):
        self.outStr='Null'
        self.modeStr='What are you doing?'
        if mode=='R':
            self.Register()
            self.modeStr='Account Registration'
        elif mode=='L':
            self.Login()
            self.modeStr='User Login'
        elif mode=='F':
            self.ForgotPass()
            self.modeStr='Password Reset'
        elif mode=='O':
            self.OutResults()
            self.modeStr='Results'
        elif mode=='C':
            self.OutResults()
            self.modeStr='Results'
        elif mode=='PR':
            self.For3()
            self.modeStr='Password Reset'
    def OutResults(self):
        if "LogB" in form: self.Log2()
        elif "ForB" in form: self.For2()
        elif "RegB" in form: self.Reg2()
        elif "ForB2" in form: self.For4()
        else:
            cnfrm=form.getfirst("c", "Null")
            if cnfrm<>"Null":
                hash=MySQLdb.escape_string(cnfrm)
                DB("UPDATE QUsers SET Qactivated='ACTIVE' WHERE Qactivated='{0}'".format(hash))
                self.outStr="Account Validated"
                
                
    
    def Reg2(self):
        usr=MySQLdb.escape_string(str(form.getvalue('Ruser')))
        pss=sha.new(MySQLdb.escape_string(str(form.getvalue('Rpass')))).hexdigest()
        ema=MySQLdb.escape_string(str(form.getvalue('Remail')))
        hsh=sha.new(usr+pss+ema+repr(time.time())).hexdigest()
        #Add Input Rule Filtering
        try:
            DB("INSERT INTO QUsers(Quser,Qpass,Qemail,Qactivated) VALUES ('{0}','{1}','{2}','{3}')".format(usr,pss,ema,hsh))
            self.sendEmail("Please confirm your account: {0}".format("https://10.33.81.87/cgi-bin/auth.py?x=C&c="+hsh),ema,"Confirmation Email")
            self.outStr="Please check your email to confirm your account"#<br><a href='{0}'>Confirm Email</a>".format("https://10.33.81.87/cgi-bin/auth.py?x=C&c="+hsh)
        except:
            self.outStr="Error. Invalid Username or Email"
    
    def Log2(self):
        usr=MySQLdb.escape_string(str(form.getvalue('Luser')))
        pss=sha.new(MySQLdb.escape_string(str(form.getvalue('Lpass')))).hexdigest()
        DB("SELECT Quser,Qrole FROM QUsers WHERE Quser='{0}' AND Qpass='{1}' AND Qactivated='ACTIVE' LIMIT 1".format(usr,pss))
        r=db.store_result()
        r=r.fetch_row()
        if len(r)==0:
            self.outStr="Login Failed."
        else:
            sss.username=r[0][0]
            userCookie=sss.cookie['sid'].value#str.split(str(sss.cookie['sid']),'=')[1]#sss.cookie['sid']
            self.outStr="Login Sucessful!"
            DB("UPDATE QUsers SET Qcookie='{0}' WHERE Quser='{1}'".format(userCookie,usr))
    
    def For2(self):
        try:
            ema=MySQLdb.escape_string(str(form.getvalue('Femail')))
            salt=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(15))
            hsh=sha.new(ema+repr(time.time())+salt).hexdigest()
            DB("UPDATE QUsers SET Qreset='{0}' WHERE Qemail='{1}'".format(hsh,ema))
            self.sendEmail("https://10.33.81.87/cgi-bin/auth.py?x=PR&k={0}".format(hsh),ema,"Password Reset")
            self.outStr="Password reset email sent"
        except: 
            self.outStr="Invalid email"

    def For3(self):   
        try:
            hsh=MySQLdb.escape_string(str(form.getfirst("k", "NullNull")))
            DB("SELECT Quser,Qemail FROM QUsers WHERE Qreset='{0}' LIMIT 1".format(hsh))
            r=db.store_result()
            r=r.fetch_row()
            if len(r)==0:
                self.outStr="Invalid Request"
            else:
                usr=r[0][0]
                ema=r[0][1]
                self.outStr="""
<form action='auth.py?x=O' method = 'POST'>
New Password: <input type='password' name='Fpass'><br>
<input type='submit' name='ForB2' value='Submit'>
<input type='hidden' name='Forhsh' value='{0}'>
</form> <p>""".format(hsh)
        except:
            pass        
    
    def For4(self):
        hsh=MySQLdb.escape_string(str(form.getvalue('Forhsh')))
        pss=sha.new(MySQLdb.escape_string(str(form.getvalue('Fpass')))).hexdigest()
        try:
            DB("UPDATE QUsers SET Qpass='{1}',Qreset='NULL' WHERE Qreset='{0}'".format(hsh,pss))
            self.outStr="Password Reset"
        except:
            self.outStr="Error"
    def sendEmail(self,msg,rcpt,subj):
        t = Thread(target=self.sendMail, args=(msg,rcpt,subj))    
        t.start()
        
    def sendMail(self,message,rcpt,subj):
        msg = MIMEText(message)
        msg['Subject']=subj
        msg['From']='CSCI465@liberty.edu'
        msg['to']=rcpt
        s = smtplib.SMTP('mail.liberty.edu')
        blah=s.ehlo()
        s.sendmail('CSCI465@liberty.edu', [rcpt], msg.as_string())
        s.quit()
    
    def Register(self):
        self.outStr="""
<form action='auth.py?x=O' method = 'POST'>
Username: <input type='text' name='Ruser'><br>
Password: <input type='password' name ='Rpass'><br>
Email: <input type='text' name='Remail'><br>
<input type='submit' name='RegB' value='Register'>
</form> <p>"""
    
    def Login(self):
        self.outStr="""
<form action='auth.py?x=O' method = 'POST'>
Username: <input type='text' name='Luser'><br>
Password: <input type='password' name ='Lpass'><br>
<input type='submit' name='LogB' value='Login'>
</form> <p>"""
    
    def ForgotPass(self):
        self.outStr="""
<form action='auth.py?x=O' method = 'POST'>
Account Email: <input type='text' name='Femail'><br>
<input type='submit' name='ForB' value='Submit'>
</form> <p>"""
    def CreatePage(self):
        return self.outStr
        
Bidoof=Auth(form.getfirst("x", "Null"))

try:
    print sss.setCookie()

    print "Content-Type: text/html"
    print """
<html><head><title>User Management</title></head>
<body><h1>User Management</h1>
<hr>
<b>{0}: </b><br>
""".format(Bidoof.modeStr)
    print "{0}".format(Bidoof.CreatePage())
    print "<hr>Currently viewing as: {0}".format(sss.getUser())
    print "<br><a href='mystery.py'>Home</a><br><a href='auth.py?x=R'>Register</a> <a href='auth.py?x=L'>Login</a> <a href='auth.py?x=F'>Forgot Password?</a>"
    print "</body></html>"
except:
    #Errors only printed for localhost
    if ClientIP<>'127.0.0.1':
        print """\
<html><body>
Whoa there
</body></html>
"""