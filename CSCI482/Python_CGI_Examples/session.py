import sha, shelve, time, Cookie, os, MySQLdb
DBServer='127.0.0.1'
DBUser=''
DBPass=''
DBName=''
db = MySQLdb.connection(host=DBServer,user=DBUser,passwd=DBPass,db=DBName)
DB = db.query

class Session(object):

   def __init__(self, expires=None, cookie_path=None):
      string_cookie = os.environ.get('HTTP_COOKIE', '')
      self.cookie = Cookie.SimpleCookie()
      self.cookie.load(string_cookie)
      self.username="Anonymous User"
      self.LI=0

      if self.cookie.get('sid'):
         sid = self.cookie['sid'].value
         #Check for existing state:
         DB("SELECT Quser,Qrole FROM QUsers WHERE Qcookie='{0}' LIMIT 1".format(sid))
         r=db.store_result()
         r=r.fetch_row()
         if len(r)>0:
             self.username=r[0][0]
             self.LI=1
         
         # Clear session cookie from other cookies
         self.cookie.clear()

      else:
         self.cookie.clear()
         sid = sha.new("VAWVrV4ea3VAV"+repr(time.time())).hexdigest()

      self.cookie['sid'] = sid

      #if cookie_path:
      #   self.cookie['sid']['path'] = cookie_path

      #session_dir = os.environ['DOCUMENT_ROOT'] + '/session'
      #if not os.path.exists(session_dir):
      #   try:
      #      os.mkdir(session_dir, 02770)
      #   # If the apache user can't create it create it manualy
      #   except OSError, e:
      #      errmsg =  """%s when trying to create the session directory. \
      #Create it as '%s'""" % (e.strerror, os.path.abspath(session_dir))
      #      raise OSError, errmsg
      #self.data = 'Blah'
      #os.chmod(session_dir + '/sess_' + sid, 0660)
      
      # Initializes the expires data
      #if not self.data.get('cookie'):
      #   self.data['cookie'] = {'expires':''}

      self.set_expires(60*60)

   #def close(self):
   #   self.data.close()

   def set_expires(self, expires=None):
      #if expires == '':
      #   self.data['cookie']['expires'] = ''
      #elif isinstance(expires, int):
      #   self.data['cookie']['expires'] = expires
      self.cookie['sid']['expires'] = expires

   def setCookie(self):
      return self.cookie.output()
   def loggedIn(self):
      return self.LI
   def getUser(self):
      return self.username

