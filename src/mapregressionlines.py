import glob


def collect_coverage():
    line_cov = []
    gcovfiles = sorted(glob.glob('*.gcov'))
    for f in gcovfiles:
            for l in open(f):
                    
                    ls = l.split()
                    f = f.replace('.gcov', '')
                    # print l
                    if (ls[0] == "-:"):
                        pass # none executable
                    elif (ls[0] == "#####:"):
                        lineno = int(ls[1].split(':')[0])
                        print lineno
                        line_cov.append((f,lineno))
                    elif ':' in ls[1]:
                        # covered 
                        lineno = int(ls[1].split(':')[0])
                        line_cov.append((f,lineno))
 

                   

                   
    return line_cov
covs = collect_coverage()
print covs

bug1294 = [('jsapi.c', 602, 620),('jsobj.c', 917, 920),('jsopcode.c', 2532, 2540)]
bug95   = [('jsobj.c', 2907, 2907),('jsobj.c', 2926, 2948),('jsobj.c', 2945, 2946),('jsobj.c', 2954, 2954)]
bug297  = [('jsopcode.c', 2889)]
bug880  = [('jsparse.c', 1625 ,1625 ),('jsparse.c', 1628, 1628 ),('jsparse.c', 1630, 1630 ),('jsparse.c', 1634, 1637),('jsparse.c', 1704, 1706)]
bug1172 = [('jsopcode.c', 985, 996),('jsopcode.c', 3075, 3077),('jsopcode.c', 3094, 3094),('jsopcode.c', 3147, 3147),('jsopcode.c', 3161, 3162)]
bug297_2 = [('jsinterop.c', 1548,1548), ('jsparse.c',1597,1639), ('jsxml.c', 1761,1761), ('jsxml.c', 1774,1774), ('jsxml.c', 1807,1810)]
bug115 = [('jsinterop.c', 318,322), ('jsinterop.c', 466,466), ('jsinterop.c', 491,499), ('jsinterop.c', 512,514),('jsinterop.c', 926,930),('jsinterop.c', 931,1005)]

bugs = [bug95, bug297, bug115, bug880, bug1172, bug1294, bug297_2]

for b in bugs:
    for (f, low, hi) in b:
        for i in range(low, hi + 1):
            print (f,i), covs.index((f,i))
        

