import os
import subprocess
import sys
import re
origWD = os.getcwd()

statalocwin="C:/Program Files (x86)/Stata13/StataMP-64.exe"
statalocmac="/Applications/Stata/StataSE.app/Contents/MacOS"
print("Wait for the message 'DONE' to show up. The Stata dofile run in the background so it might seem like the program is finished when it isn't")

def parse_location(fileloc):
	filepath = fileloc.split("/")
	script = filepath[-1]
	scriptdir = "/".join(filepath[0:-1])
	return script, scriptdir

def run_stata(fileloc):
	"""Run stata dofile in batch mode, deletes the log file and fix the working directory"""
	script, scriptdir = parse_location(fileloc)
	os.chdir(scriptdir)

	if sys.platform == "win32":
		subprocess.call([statalocwin, "-e", "do", script])
	else:
		subprocess.call([statalocmac, "-b", "do", script])
	
	err=re.compile("^r\([0-9]+\);$")
	with open("{}.log".format(script[0:-3]), 'r') as logfile:
		for line in logfile:
			if err.match(line):
				sys.exit("Stata Error code {line} in {fileloc}".format(line=line[0:-2], fileloc=fileloc) )

	os.remove("{}.log".format(script[0:-3]))
	os.chdir(origWD)

def run_python(fileloc):
	"""Run Python script and fix the working directory"""
	script, scriptdir = parse_location(fileloc)
	os.chdir(scriptdir)
	subprocess.call(["python", script])  
	os.chdir(origWD)

def run_R(fileloc):
	"""Run R script and fix the working directory"""
	script, scriptdir = parse_location(fileloc)
	os.chdir(scriptdir)
	subprocess.call(["Rscript", "--vanilla", script])
	os.chdir(origWD)

def run_latex(fileloc):
	"""Run a Tex script, run bibtex and then the Tex script twice more. Then fix the working directory"""
	script, scriptdir = parse_location(fileloc)
	os.chdir(scriptdir)
	subprocess.call(["pdflatex", script])
	subprocess.call(["bibtex", script[0:-4] ])
	subprocess.call(["pdflatex", script])
	subprocess.call(["pdflatex", script])
	os.chdir(origWD)




##########################################################
# Actual Do-Files/Scripts/R-codes
##########################################################


###Note: Please keep the first parts that clean the data fixed and untouched

#eg templates:
# run_python("analysis/STATA/SY_Explore_231206/merge.py")
# run_R("analysis/graphing.r")
# run_stata("analysis//analysis.do")
# run_latex("analysis/Paper.tex")


###1. Data Cleaning
run_stata("stata_test.do")




















# #Clean up intermediate files
# os.remove("01_Data/02_Clean/appended.csv")
# os.remove("02_Output/balance.jpg")
# os.remove("02_Output/results.tex")
# os.remove("03_Paper/Paper.aux")



