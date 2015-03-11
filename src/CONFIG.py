import os

curdir = os.getcwd()+ os.sep

JS = "/scratch/papers/icst2015paper/js1.6/src/Linux_All_DBG.OBJ/js -f "
#"../js1.6/Linux_All_DBG.OBJ/js -f "
GCOVDIR = "/scratch/papers/icst2015paper/js1.6/src/Linux_All_DBG.OBJ/"

OBJDIR  = "/scratch/papers/icst2015paper/js1.6/src/Linux_All_DBG.OBJ/"

FILENAMES = ["js", "jsapi","jscpucfg","jsexn","jslog2",	"jsobj","jsscope","jsarena","jsdate","jsfun","jslong",
	"jsopcode", "jsscript", "jsarray",  "jsdbgapi","jsgc", "jsmath", "jsparse", "jsstr",
	"jsatom", "jsdhash", "jshash", "jsmathtemp", "jsprf", "jsutil",
	"jsbool", "jsdtoa",  "jsinterp", "jsnum", "jsregexp", "jsxdrapi",
	"jscntxt", "jsemit", "jslock", "jsscan", "jsxml"]
ITER = 0

possibleModes = ["line","n_line", "fun","n_fun", "branch"]

mode = possibleModes[0]
