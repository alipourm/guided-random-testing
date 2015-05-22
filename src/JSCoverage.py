import sys
import subprocess
import os
import JSCONFIG as CONFIG
import commands
import glob
import time
from myutils import InfiniteLoopError
import numpy as np


def execute(cmd):
    status, output = commands.getstatusoutput(cmd)
   # print cmd,output
    return status, output
 


class Coverage: 
    def __init__(self, test):
        self.JS = CONFIG.JS
        self.GCOVDIR = CONFIG.GCOVDIR
        self.OBJDIR = CONFIG.OBJDIR
        self.SRCDIR = CONFIG.SRCDIR
        self.line_cov   = []
        self.line_ncov   = []
        self.branch_cov = []
        self.function_cov = []
        self.function_ncov = []
        self.tc = test
        self.elapsed = 0
        self.functions = []
        self.vgrun = self.tc +".vgrun"
        self.calculate()

  

    def calculate(self):
        execute("rm -rf " + self.OBJDIR + "*.gcda")
        execute("rm -rf " + self.GCOVDIR + "*.gcov")
        self.executetc()
        for f in glob.glob(self.SRCDIR + "*.c"):
           execute("gcov  -o {0} {1}".format(CONFIG.OBJDIR, f))
        self.collect_coverage()




    def executetc(self, js=None):
        test = self.tc
        vgrun = self.vgrun
        execute("cp jsfunrun.js " + vgrun)
        execute("cat " + test + " >> " + vgrun)
        out = open(vgrun, 'a')
        out.write('\ndumpln("ALL OK");\n')
        out.flush()
        out.close()

        if js is None:
            status, output =  execute('timeout 10 ' + self.JS + " " + vgrun) 
        else:
            status, output =  execute('timeout 10 ' + js + " -f  " + vgrun) 
        execute("rm -f " + self.vgrun) 
            
        if status == 124: # timeout
            raise InfiniteLoopError(self.tc)
        self.output = output
        return output


    def collect_coverage(self):
        gcovfiles = sorted(glob.glob('*.gcov'))
        for f in gcovfiles:
            for l in open(f):
                    ls = l.split()
                    # print l
                    if (ls[0] == "-:"):
                        pass # none executable
                    elif (ls[0] == "#####:"):
                        # not covered
                        self.line_cov.append(0)
                        self.line_ncov.append(0)
                    elif ':' in ls[1]:
                        # covered 
                        self.line_cov.append(1)
                        self.line_ncov.append(int(ls[0].split(":")[0]))
                    elif ls[0] == "function":
                        self.function_cov.append(min(1, int(ls[3])))
                        self.function_ncov.append(int(ls[3]))

    
        

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
        return float(np.sum(self.line_cov))/len(self.line_cov)

    def get_percent_branch(self):
        return float(np.sum(self.branch_cov))/len(self.branch_cov)

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

