#!python
# coding:UTF-8 
import json

def rec(inV):
    if type(inV)==dict:
        print "<Dict>"
        for i in inV.keys():
            print "<{0}>".format(i)
            rec(inV[i])
            print "</{0}>".format(i)
        print "</Dict>"
    elif type(inV)==list:
        print "<List>"
        for i in inV:
            rec(i)
        print "</List>"
    #elif inV==None:
    #    return
    else:
        print json.dumps(inV)
        #str(inV).decode('utf-8', 'ignore').encode('utf-8')#.encode('ascii','backslashreplace')#("utf-16")
        return
    

with open("data.json") as f:
    data=json.load(f)
    print rec(data)

