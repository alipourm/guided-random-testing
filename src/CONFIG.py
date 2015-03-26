import os

curdir = os.getcwd()+ os.sep

JS = curdir + 'js1.6/src/Linux_All_DBG.OBJ/js -f '

GCOVDIR = curdir + 'js1.6/src/'

OBJDIR  = curdir + "js1.6/src/Linux_All_DBG.OBJ/"

FILENAMES = ["js", "jsapi","jscpucfg","jsexn","jslog2",	"jsobj","jsscope","jsarena","jsdate","jsfun","jslong",
	"jsopcode", "jsscript", "jsarray",  "jsdbgapi","jsgc", "jsmath", "jsparse", "jsstr",
	"jsatom", "jsdhash", "jshash", "jsmathtemp", "jsprf", "jsutil",
	"jsbool", "jsdtoa",  "jsinterp", "jsnum", "jsregexp", "jsxdrapi",
	"jscntxt", "jsemit", "jslock", "jsscan", "jsxml"]


possibleModes = ["line","n_line", "fun","n_fun", "branch"]

mode = possibleModes[0]
