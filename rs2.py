#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
	.____    ____    ____
	|  _ \  / ___|  |___ \
	| |_) | \___ \    __) |
	|  _ <   ___) |  / __/
	|_| \_\ |____/  |_____|


Name: RS2
Author: K4YT3X
Date: 3/18/17

Contributor: Terrance@askubuntu.com

(C) 2017 K4YT3X

Licensed under the GNU General Public License Version 3 (GNU GPL v3),
	available at: https://www.gnu.org/licenses/gpl-3.0.txt

Description: RS2 is a Linux Terminal extender. RS2 adds timestamp to all commands and
it also has a customized prompt (PS1) that is sensitive to user. It's kind of powerful
and also kind of interesting. Explore it yourself.

"""
import os
import datetime
import sys

VERSION = '1.2'
USRHOME = os.getenv("HOME")
OVERWRITE = False

bashR2 = []  # Set as global cuz needed during uninstallation
bashR2.append("# RS2\n")
bashR2.append("if [ -f \"$HOME/.rs2\" ]; then\n")
bashR2.append("    . \"$HOME/.rs2\"\n")  # Basically calls rs2 script in terminal
bashR2.append("fi\n")


# ------------------------------ Begin Classes

class kcs():
	"""
		OLD K4T Color Standard (Now Avalon Color Framework)
		Defines color and standardizes output
	"""

	# Define Global Color
	global W, R, G, OR, Y, B, P, C, GR, H, BD, NH
	# Console colors
	# Unix Console colors
	W = '\033[0m'  # white (normal / reset)
	R = '\033[31m'  # red
	G = '\033[32m'  # green
	OR = '\033[33m'  # orange
	Y = '\033[93m'  # yellow
	B = '\033[34m'  # blue
	P = '\033[35m'  # purple
	C = '\033[96m'  # cyan
	GR = '\033[37m'  # grey
	H = '\033[8m'  # hidden
	BD = '\033[1m'  # Bold
	NH = '\033[28m'  # not hidden

	def info(msg):
		print(G + '[+] INFO: ' + str(msg) + W)

	def tInfo(msg):
		print(W + str(datetime.datetime.now()) + G + ' [+] INFO: ' + str(msg) + W)

	def subLevelInfo(msg):
		print(W + str(datetime.datetime.now()) + GR + ' [+] INFO: ' + str(msg) + W)

	def warning(msg):
		print(Y + BD + '[!] WARNING: ' + str(msg) + W)

	def error(msg):
		print(R + BD + '[!] ERROR: ' + str(msg) + W)

	def debug(msg):
		print(R + BD + '[*] DBG: ' + str(msg) + W)

	def input(msg):
		res = input(Y + BD + '[?] USER: ' + msg + W)
		return res

	def ask(msg, default=False):
		if default is False:
			while True:
				ans = kcs.input(msg + ' [y/N]: ')
				if ans == '' or ans[0].upper() == 'N':
					return False
				elif ans[0].upper() == 'Y':
					return True
				else:
					kcs.error('Invalid Input!')
		elif default is True:
			while True:
				ans = kcs.input(msg + ' [Y/n]: ')
				if ans == '' or ans[0].upper() == 'Y':
					return True
				elif ans[0].upper() == 'N':
					return False
				else:
					kcs.error('Invalid Input!')
		else:
			raise TypeError('invalid type for positional argument: \' default\'')


# ------------------------------ Begin Functions

def writeRS2():
	"""
		Writes RS2 Script to $Home/.rs2
	"""
	global OVERWRITE
	rs2 = []  # Why not just include the entire file in code?
	rs2.append("#RS2 Terminal Timestamp by K4YT3X\n")
	rs2.append("#Modified from original script by Terrance@askubuntu.com\n")
	rs2.append("\n")
	rs2.append("# Fill with minuses\n")
	rs2.append("# (this is recalculated every time the prompt is shown in function prompt_command):\n")
	rs2.append("fill=\"--- \"\n")
	rs2.append("\n")
	rs2.append("timestamp=\"true\"\n")
	rs2.append("reset_style=\'\\[\\033[00m\\]\'\n")
	rs2.append("status_style=$reset_style\'\\[\\033[0;90m\\]\' # gray color; use 0;37m for lighter color\n")
	rs2.append("command_style=$reset_style\'\\[\\033[1;29m\\]\' # bold black\n")
	rs2.append("\n")
	rs2.append("# Special Blue for root\n")
	rs2.append("a=$(id|awk -F\\( \'{print $1}\')\n")
	rs2.append("if [ \"$a\" = \"uid=0\" ]\n")
	rs2.append("then\n")
	rs2.append("    # for root\n")
	rs2.append("    user_color=\'\\[\\033[94m\\]\'\n")
	rs2.append("    dir_color=\'\\[\\033[34m\\]\'\n")
	rs2.append("else\n")
	rs2.append("    # for other users\n")
	rs2.append("    user_color=\'\\[\\033[93m\\]\'\n")
	rs2.append("    dir_color=\'\\[\\033[33m\\]\'\n")
	rs2.append("fi\n")
	rs2.append("\n")
	rs2.append("# Prompt variable:\n")
	rs2.append("if [ \"$timestamp\" = \"true\" ]\n")
	rs2.append("then\n")
	rs2.append("    PS1=\"$status_style\"\'$fill $(date +\"%m/%d/%y \")\\t\\n\'\'${debian_chroot:+($debian_chroot)}\'$user_color\'\\u\\[\\033[00m\\]\\$\\[\\033[90m\\]\\h\'$dir_color\'\'[\'\\w\']\'\\[\\033[00m\\]> \'\n")
	rs2.append("else\n")
	rs2.append("    PS1=\'${debian_chroot:+($debian_chroot)}\'$user_color\'\\u\\[\\033[00m\\]\\$\\[\\033[90m\\]\\h\'$dir_color\'\'[\'\\w\']\'\\[\\033[00m\\]> \'\n")
	rs2.append("fi\n")
	rs2.append("\n")
	rs2.append("# Reset color for command output\n")
	rs2.append("# (this one is invoked every time before a command is executed):\n")
	rs2.append("trap \'echo -ne \"\\033[00m\"\' DEBUG\n")
	rs2.append("\n")
	rs2.append("function prompt_command {\n")
	rs2.append("# create a $fill of all screen width minus the time string and a space:\n")
	rs2.append("let fillsize=${COLUMNS}-18\n")
	rs2.append("fill=\"\"\n")
	rs2.append("while [ \"$fillsize\" -gt \"0\" ]\n")
	rs2.append("do\n")
	rs2.append("    fill=\"-${fill}\" # fill with underscores to work on\n")
	rs2.append("    let fillsize=${fillsize}-1\n")
	rs2.append("done\n")
	rs2.append("\n")
	rs2.append("# If this is an xterm set the title to user@host:dir\n")
	rs2.append("case \"$TERM\" in\n")
	rs2.append("    xterm*|rxvt*)\n")
	rs2.append("    bname=$(basename \"${PWD/$HOME/~}\")\n")
	rs2.append("    echo -ne \"\\033]0;${bname}: ${USER}@${HOSTNAME}: ${PWD/$HOME/~}\\007\"\n")
	rs2.append("    ;;\n")
	rs2.append("    *)\n")
	rs2.append("    ;;\n")
	rs2.append("esac\n")
	rs2.append("}\n")
	rs2.append("\n")
	rs2.append("PROMPT_COMMAND=prompt_command\n")
	if os.path.isfile(USRHOME + '/.rs2'):
		if not kcs.ask('RS2 Already Installed, Overwrite?'):
			kcs.warning('Aborting')
			exit(0)
	kcs.info(Y + BD + 'Installing .rs2 Script')
	with open(USRHOME + '/.rs2', 'w') as r2:
		for line in rs2:
			kcs.subLevelInfo('write: \"' + line.strip('\n') + '\"')
			r2.write(line)
	r2.close()


def writeBashRc():
	"""
		Writes RS2 Script into #HOME/.bashrc
	"""
	global OVERWRITE
	installed = False
	with open(USRHOME + '/.bashrc', 'r') as bashrc:
		for line in bashrc:
			if 'RS2' in line:
				installed = True
	bashrc.close()
	kcs.info(Y + BD + 'Installing RS2 .bashrc Script')
	with open(USRHOME + '/.bashrc', 'a+') as bashrc_append:
		if installed:
			kcs.warning('RS2 Script Already Installed in .bashrc, skipping...')
		else:
			for line in bashR2:
				kcs.subLevelInfo('write: \"' + line.strip('\n') + '\"')
				bashrc_append.write(line)
	bashrc_append.close()


def uninstallRS2():
	"""
		Remove RS2 Completely
	"""
	o_bashrc = []
	try:
		os.remove(USRHOME + '/.rs2')
	except FileNotFoundError:
		pass
	skip = 0
	with open(USRHOME + '/.bashrc', 'r') as bashrc:
		for line in bashrc:
			if '# RS2' in line:
				skip += 1
			if skip == 0 or skip > 4:
				o_bashrc.append(line)
			else:
				skip += 1
				continue
	bashrc.close()
	try:
		os.remove(USRHOME + '/.bashrc')
	except FileNotFoundError:
		pass
	with open(USRHOME + '/.bashrc', 'w') as bashrc_write:
		for line in o_bashrc:
			bashrc_write.write(line)
	bashrc_write.close()


def printIcon():
	print(R + ' ____    ____  ' + OR + '  ____' + W)
	print(R + '|  _ \  / ___| ' + OR + ' |___ \\' + W)
	print(R + '| |_) | \___ \ ' + OR + '   __) |' + W)
	print(R + '|  _ <   ___) |' + OR + '  / __/' + W)
	print(R + '|_| \_\ |____/ ' + OR + ' |_____|\n' + W)


def printHelp():
	if os.path.isfile(USRHOME + '/.rs2'):
		print(W + '[' + G + '+' + W + ']' + W + BD + ' RS2 Status: ' + G + BD + 'Installed' + W)
	else:
		print(W + '[' + R + 'x' + W + ']' + W + BD + ' RS2 Status: ' + R + BD + 'Not Installed' + W)
	print(BD + '\nUsage: 	python3 ' + __file__ + ' [install] [uninstall]' + W)
	if __file__ != 'rs2.py' and __file__.split('/')[-1] != 'rs2.py':
		print(OR + 'Why did you change the file name???')  # Just for fun
	print()
	print(Y + BD + 'install' + W + ': install RS2 for current user')
	print(R + BD + 'uninstall' + W + ': remove installed RS2')
	print(GR + '--help / -h: print this help page')


# ------------------------------ Begin Procedural

printIcon()  # Print the icon anyway

try:
	if sys.argv[1] == 'uninstall':
		if kcs.ask('Confirm Removal'):
			kcs.info('Removing...')
			uninstallRS2()
			kcs.info('Removal Complete!')
			exit(0)
		else:
			kcs.warning('Removal Canceled!')
			exit(0)
	elif sys.argv[1] == 'install':
		if kcs.ask('Confirm Install'):
			writeRS2()
			writeBashRc()
			kcs.info('Installation Successful!')
		else:
			kcs.warning('Installation Canceled!')
	elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
		printHelp()
	else:
		kcs.error('Invalid Parameter')
		printHelp()
except IndexError:  # When no arguments given
	printHelp()
