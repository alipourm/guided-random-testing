import sys
import os
import GCCCONFIG
import commands
import glob
from myutils import InfiniteLoopError
from numpy import sum


def execute(cmd):
    status, output = commands.getstatusoutput(cmd)
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
        execute("rm -rf " + "*.gcov")
        self.executetc()
        olddir = os.getcwd()
#        os.chdir(self.OBJDIR)
        for f in glob.glob(self.OBJDIR +'*.gcno'):
            gcov_cmd = "gcov -o {0} {1}".format(self.OBJDIR, f)
            status, output = execute(gcov_cmd)
#        os.chdir(olddir)
        self.collect_coverage()




    def executetc(self, js=None):
        test = self.tc
        status, output =  execute('timeout 30 ' + self.executable + " " + test)
        if status == 124: # timeout
            raise InfiniteLoopError(self.tc)

        return output

    
    def get_mapping(self):
        code_cov_map = {}
        i = 0
        gcovfiles = sorted(glob.glob('*.gcov'))
        for f in gcovfiles:
            for l in open(f).readlines():
                    ls = l.strip().split(':')
                    if (ls[0] == '-'):
                        pass # none executable
                    elif (ls[0] == "#####"):
                        # not covered
                        line_no = int(ls[1].strip())
                        code_cov_map[f, line_no] = i
                        i += 1
                    elif ls[0].isdigit():
                        # covered 
                        line_no = int(ls[1].strip())
                        code_cov_map[f, line_no] = i
                        i += 1
                    else:
                        # logically funny, just to keep other things in the the case needed
                        assert (0)
        return code_cov_map

    def collect_coverage(self):
        gcovfiles = sorted(glob.glob('*.gcov'))
        for f in gcovfiles:
            for l in open(f).readlines():
                    ls = l.strip().split(':')
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

    def get_percent_line(self):
        return float(sum(self.line_cov))/len(self.line_cov)
