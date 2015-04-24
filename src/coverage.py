import sys
import subprocess
import os
import GCCCONFIG
import commands
import glob
import time




def isSubsumed(cov1, cov2):  # cov1 = cov2 - extra + loss
    if len(cov1) != len(cov2):
        print "ERROR: incomparable coverage vectors"
    k = {}
    loss  = 0
    extra = 0 
    for i in range(0, len(cov1)):
        if cov2[i] > 0 and cov1[i] == 0:
            extra += 1
        elif cov1[i] > 0 and cov2[i] == 0:
            loss  += 1
    k["loss"] = loss
    k["extra"]= extra
    return k

class InfiniteLoopError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return 'Inifinte Loop in ' + repr(value)


def execute(cmd):
    status , output = commands.getstatusoutput(cmd)
    return status, output
 


class Coverage: 

    def __init__(self, test):
        self.executable = GCCCONFIG.GCC
        self.GCOVDIR = GCCCONFIG.GCOVDIR
        self.OBJDIR = GCCCONFIG.OBJDIR
        self.SRCDIR = GCCCONFIG.SRCDIR
        self.line_cov   = []
        self.line_ncov   = []
        self.branch_cov = []
        self.function_cov = []
        self.function_ncov = []
        self.tc = test
        self.elapsed = 0
        self.functions = []
        self.calculate()
        # self.executetc()


  

    def calculate(self):
        execute("rm -rf " + self.OBJDIR + "*.gcda")
        execute("rm -rf " + self.GCOVDIR + "*.gcov")
        self.executetc()
        olddir = os.getcwd()
        os.chdir(self.OBJDIR)
        for f in glob.glob('*.gcda'):
            gcov_cmd = "gcov {0}".format(f)
            status, output = execute(gcov_cmd)
        os.chdir(olddir)
        self.collect_coverage()




    def executetc(self, js=None):
        test = self.tc
        status, output =  execute('timeout 10 ' + self.executable + " " + test) 
        if status == 124: # timeout
            raise InfiniteLoopError(self.tc)

        return output


    def collect_coverage(self):
        gcovfiles = sorted(glob.glob(self.GCOVDIR + '*.gcov'))
        for f in gcovfiles:
#            print f
        
            for l in open(f).readlines():
                    ls = l.strip().split(':')
                    
#                    print f, l , ls

                    if (ls[0] == '-'):
                        pass # none executable
                    elif (ls[0] == "#####"):
                        # not covered
                        self.line_cov.append(0)
                        self.line_ncov.append(0)
                    elif ls[0].isdigit():
                        # covered 
                        none = False
                        self.line_cov.append(1)
                        self.line_ncov.append(int(ls[0]))
                    else:
                        # logically funny, just to keep other things in the the case needed
                        assert (0)
                        continue
        


 
    
        

    def choose(self,mode):
        possibleModes = ["line","n_line", "fun","n_fun", "branch"]
            
        if mode == "line":
            return self.get_l_cov()
        elif mode == "n_line":
            return self.get_nl_cov()
        elif mode == "fun":
            return self.get_f_cov()
        elif mode == "n_fun":
            return self.get_nf_cov()
        elif mode == "branch":
            return self.get_b_cov()
        else:
            print "ERROR: Coverage mode is not present. \
            Please define the corresponing coverage function."
            sys.exit(-1)

    def get_l_cov(self):
        return self.line_cov

    def get_nl_cov(self):
        return self.line_ncov

    def get_b_cov(self):
        return self.branch_cov

    def get_f_cov(self):
        return self.function_cov

    def get_nf_cov(self):
        return self.function_ncov

    def get_percent_line(self):
       
        return float(sum(self.line_cov))/len(self.line_cov)

    def get_percent_branch(self):
        k = [l for l in self.branch_cov if l != 0]
        return float(len(k))/len(self.branch_cov)

    def get_percent_function(self):
        k = [l for l in self.function_cov if l != 0]
        return float(len(k))/len(self.function_cov)

    def get_total_line(self):
        k = [l for l in self.line_cov if l != 0]
        return len(k)

    def get_total_branch(self):
        k = [l for l in self.branch_cov if l != 0]
        return len(k)

    def get_total_function(self):
        k = [l for l in self.function_cov if l != 0]
        return len(k)
