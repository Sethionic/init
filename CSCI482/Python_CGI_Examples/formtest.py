#!/usr/bin/env python
import cgi,time,Cookie,os,sha
form = cgi.FieldStorage()

DBServer='127.0.0.1'
DBUser=''
DBPass=''
DBName=''
db = MySQLdb.connection(host=DBServer,user=DBUser,passwd=DBPass,db=DBName)
DB = db.query

# getlist() returns a list containing the
# values of the fields with the given name
colors = form.getlist('color')

print "Content-Type: text/html"
print
print '<html><body>'
print 'The colors list:', colors
for color in colors:
   print '<p>', cgi.escape(color), '</p>'
print '</body></html>'

print """\
<html><body>
<form method="post" action="formtest.py">
Red<input type="checkbox" name="color" value="red">
Green<input type="checkbox" name="color" value="green">
<input type="submit" value="Submit">
</form>
<br>Test: {0}
</body></html>
""".format(sss.testString())