import sys
import subprocess
import os
import CONFIG
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


class Coverage: 
    def execute(self,cmd):
        status , output = commands.getstatusoutput(cmd)
        print cmd, output

    def __init__(self, test):
        self.JS = CONFIG.JS
        self.GCOVDIR = CONFIG.GCOVDIR
        self.OBJDIR = CONFIG.OBJDIR
        self.line_cov   = []
        self.line_ncov   = []
        self.branch_cov = []
        self.function_cov = []
        self.function_ncov = []
        self.tc = test
        self.elapsed = 0
        self.functions = []
        self.calculate()

    def get_time(self):
        return self.elapsed

    def calculate(self):
        test = self.tc
        self.execute("rm -rf " + self.OBJDIR + "*.gcda")
        self.execute("rm -rf " + self.OBJDIR + "*.gcov")
        self.execute("rm -rf " + self.GCOVDIR + "*.gcda")
        self.execute("rm -rf " + self.GCOVDIR + "*.gcov")
        vgrun = "vgrun_" + test.split("/")[-1] +".js"
        self.execute("cp jsfunrun.js " + vgrun)
        self.execute("cat " + test + " >> " + vgrun)
        # Write input to `vgrun.js'
        out = open(vgrun, 'a')
        out.write('\ndumpln("ALL OK");\n')
        out.flush()
        out.close()
        start_time = time.time()
        self.execute(self.JS + " " + vgrun   )
        self.elapsed = time.time() - start_time
        oldpath = os.getcwd()
        os.chdir(self.GCOVDIR)
       
        self.execute("gcov js  -o " + self.OBJDIR )
        for f in glob.glob(self.GCOVDIR + "*.c"):
            self.execute("gcov -f -b " + f)
        for f in glob.glob(self.GCOVDIR + "*.o"):
            self.execute("gcov -f -b --object-file " + f)
        for f in glob.glob(self.GCOVDIR + "*.so"):
            self.execute("gcov -f -b " + f + " ")
        for f in glob.glob(self.GCOVDIR + "*.a"):
            self.execute("gcov -f -b " + f)
        gcovfiles = os.listdir(os.getcwd())
        GCOVDIR = os.getcwd()+os.sep

        os.chdir(oldpath)
        gcovfiles = sorted(gcovfiles)
        # print 'gcovfiles:', gcovfiles
        for f in gcovfiles:
            if ".gcov" in f:
                print f
                for l in open(GCOVDIR + f):
                    ls = l.split();
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
                        if 'JS_Convert' in ls:
                            print 'fn:', ls[3]
                        
                        if min(1, int(ls[3])) == 1:
                            self.functions.append(f + ':' + ls[1])

                    elif ls[0] == "branch":
                        if ls[1] != "never" and ls[3] != "0%":
                            self.branch_cov.append(1)
                        else:
                            self.branch_cov.append(0)



        # subprocess.call(["rm -rf " + self.OBJDIR + "*.gcda"], shell=True)
        # subprocess.call(["rm -rf " + self.GCOVDIR + "*.gcov"], shell=True)
        # subprocess.call(["rm -rf " + vgrun], shell=True)
        

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
        k = [l for l in self.line_cov if l != 0]
        return float(len(k))/len(self.line_cov)

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
