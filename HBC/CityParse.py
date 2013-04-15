import json

with open("data.json") as f:
    data=json.load(f)
    for l1 in data:
        for l2 in l1.keys():
            print "\n\nL2 Contents: ({0})".format(l1.keys())
            for l3 in l1[l2].keys():
                if l3 == 'posts':
                    for l4 in l1[l2][l3]:
                        print " "*8+"\nL4 Contents: ({0})".format(l4.keys())
                        for l5 in l4.keys():
                            print " "*8+l5,": ",l4[l5]
                else:
                    print " "*4+l3,": ",l1[l2][l3]
            
        
            