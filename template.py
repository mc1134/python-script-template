import numpy as np
import matplotlib as plt
import random as rnd
import os, sys, ast

"""
DESCRIPTION OF SCRIPT PURPOSE AND USAGE
"""

# some helper functions
black = lambda strn:"\033[1;30m{}\033[0m".format(strn)
red = lambda strn:"\033[1;31m{}\033[0m".format(strn)
orange = lambda strn:"\033[1;38;5;208m{}\033[0m".format(strn)
green = lambda strn:"\033[1;32m{}\033[0m".format(strn)
blue = lambda strn:"\033[1;94m{}\033[0m".format(strn)
flash = lambda strn:"\033[1;5m{}\033[0m".format(strn)
charline = lambda char, length: str.join("", [char for i in range(length)])

def error(strn):
	print(red("Error: " + strn))
def warning(strn):
	print(orange("Warning: " + strn))
def info(strn):
	print(blue(strn))
def log(strn):
	print(black(strn))
def success(strn):
	print(green(strn))

SET_VALUE = "set"

##### EDIT THESE #####
# argument list
ARGS = [
#	{
#		"id": short name for the arg,
#		"name": arg to display in usage string,
#		"description": description for usage string,
#		"required": True/False,
#		"value": value to set, if given; initialized to default value
#	},
	{
		"id": "infile",
		"name": "INFILE.txt",
		"description": "The file to process...something.",
		"required": True,
		"value": None
	},
	{
		"id": "outfile",
		"name": "OUTFILE.txt",
		"description": "The file to store stuff in. Default is 'result.txt'.",
		"required": False,
		"value": "result.txt"
	}
]

def getArgByID(id):
	return ARGS[[item["id"] for item in ARGS].index(id)]

def getOptionByAbbr(abbr):
	return OPTIONS[[item["abbr"] for item in OPTIONS].index(abbr)]

# functions that execute when an option is detected
def action_a(args):
	getOptionByAbbr("a")["value"] = args[1]

def action_b(args):
	getOptionByAbbr("b")["value"] = 1

def action_D(args):
	getOptionByAbbr("D")["value"] = SET_VALUE

def action_H(args):
	getOptionByAbbr("H")["value"] = SET_VALUE

REQUIRED_OPTIONS = [
	{
		"abbr": "D",
		"name": "debug",
		"description": "Prints all args/options variable values",
		"action": action_D,
		"required": False,
		"nargs": 0,
		"value": None
	},
	{
		"abbr": "H",
		"name": "help",
		"description": "Prints the usage string and exits",
		"action": action_H,
		"required": False,
		"nargs": 0,
		"value": None
	}
]

# option list
OPTIONS = [
#	{
#		"abbr": option shorthand (a single letter),
#		"name": long name,
#		"description": description for usage string,
#		"action": function defined beforehand, always takes in the list of args (including the option tag) and parses it accordingly
#		"required": True/False,
#		"nargs": # of args, e.g. "-o file.csv" would require 1, whereas "-s" requires 0,
#		"value": set by the action if applicable, initialized to default value
#	},
	{
		"abbr": "a",
		"name": "alpha",
		"description": "Takes in an alpha value",
		"action": action_a,
		"required": True,
		"nargs": 1,
		"value": None
	},
	{
		"abbr": "b",
		"name": "beta",
		"description": "Sets beta to 1 (0 by default)",
		"action": action_b,
		"required": False,
		"nargs": 0,
		"value": 0
	}
]
OPTIONS += REQUIRED_OPTIONS
######################

argstrn = ""; maxarglen = max([len(item["name"]) for item in ARGS])
for i in range(len(ARGS)):
	argname = ARGS[i]["name"]
	argdesc = ARGS[i]["description"]
	argstrn += "{}:{}{}. {}\n".format(argname, charline(" ", maxarglen+1-len(argname)), "Required" if ARGS[i]["required"] else "Optional", argdesc)
arglist = " ".join([item["name"] for item in ARGS])

optstrn = ""; maxoptlen = max([len(item["name"]) + len(item["abbr"]) for item in OPTIONS])
for i in range(len(OPTIONS)):
	optabbr = OPTIONS[i]["abbr"]
	optname = OPTIONS[i]["name"]
	optdesc = OPTIONS[i]["description"]
	optstrn += "-{}, --{}:{}{} (args: {}).{}\n".format(optabbr, optname, charline(" ", maxoptlen+1-len(optabbr)-len(optname)), "Required" if OPTIONS[i]["required"] else "Optional", OPTIONS[i]["nargs"], optdesc)
flags = "".join([item["abbr"] for item in OPTIONS])

usage = "\
=========================== Usage ==============================\n\
python NAME.py [-{}] {}\n\
====================== Input arguments =========================\n\
{}\
========================== Options =============================\n\
{}\
========================= Examples =============================\n\
python NAME.py put_stuff_here\n\
================================================================\
".format(flags, arglist, argstrn, optstrn)

##### EDIT THIS FUNCTION #####

def dosomething():
	"""
	Description of this function
	"""
	print("Hello World!")

##############################

def debug_info():
	for item in OPTIONS:
		print("{} value: {}".format(item["name"], item["value"]))
	for item in ARGS:
		print("{} value: {}".format(item["name"], item["value"]))

def runner(args):
	info("Parsing arguments...")

	args = args[1:]
	argcounter = 0
	optabbrs = [item["abbr"] for item in OPTIONS]
	optnames = [item["name"] for item in OPTIONS]
	while len(args) > 0:
		curr_arg = args[0]
		# options
		if curr_arg[0] == "-":
			idx = 0
			if curr_arg[1] != "-" and curr_arg[1:] in optabbrs:
				idx = optabbrs.index(curr_arg[1:])
			elif curr_arg[2:] in optnames:
				idx = optnames.index(curr_arg[2:])
			else:
				warning("Option '{}' not recognized. Skipping option...".format(curr_arg))
				args = args[1:]
				continue
			try:
				OPTIONS[idx]["action"](args)
				info("    parsed option '{}'".format(curr_arg))
			except:
				warning("Could not perform action for '{}'. Skipping option...".format(curr_arg))
			args = args[1+OPTIONS[idx]["nargs"]:]
		# arguments
		elif argcounter >= len(ARGS):
			warning("Too many arguments provided. Skipping argument '{}'...".format(curr_arg))
			args = args[1:]
		else:
			ARGS[argcounter]["value"] = curr_arg
			info("    parsed argument '{}'".format(curr_arg))
			argcounter += 1
			args = args[1:]

	info("Done parsing.")

	allRequired = True
	for option in OPTIONS:
		if option["required"]:
			if not option["value"]:
				error("no value for required option {}.".format(option["name"]))
				allRequired = False
	for arg in ARGS:
		if arg["required"]:
			if not arg["value"]:
				error("no value for required argument {}.".format(arg["name"]))
				allRequired = False
	if not allRequired:
		log(usage)
		return False

	if getOptionByAbbr("D")["value"] == SET_VALUE:
		debug_info()
	if getOptionByAbbr("H")["value"] == SET_VALUE:
		log(usage)
		return True

##### may need to edit this part #####
	if getOptionByAbbr("D")["value"] == SET_VALUE:
		dosomething()
	else:
		try:
			dosomething()
		except:
			error("something went wrong.")
			return False
	return True
######################################

if __name__ == "__main__":
	success("Done.") if runner(sys.argv) else log("Exiting...")
