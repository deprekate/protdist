#!/usr/bin/env python3
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 
import os
import sys
import argparse
from argparse import RawTextHelpFormatter
from subprocess import Popen, PIPE, STDOUT
from types import MethodType
from termcolor import colored
from subprocess import Popen, PIPE, STDOUT
import tempfile


#sys.path.pop(0)
from genbank.file import File


def is_valid_file(x):
	if not os.path.exists(x):
		raise argparse.ArgumentTypeError("{0} does not exist".format(x))
	return x


if __name__ == '__main__':
	usage = '%s [-opt1, [-opt2, ...]] infile' % __file__
	parser = argparse.ArgumentParser(description='', formatter_class=RawTextHelpFormatter, usage=usage)
	parser.add_argument('infile', type=is_valid_file, help='input file')
	parser.add_argument('-o', '--outfile', action="store", default=sys.stdout, type=argparse.FileType('w'), help='where to write output [stdout]')
	args = parser.parse_args()

	f = tempfile.NamedTemporaryFile(delete=False)

	try:
		output = Popen(["clustalw", "-output=gcg", "-matrix=BLOSUM", "-outfile="+f.name,"-ktuple=2", "-infile="+args.infile], stdout=PIPE, stdin=PIPE, stderr=PIPE).stdout.read()
	except:
		sys.stderr.write("Warning: clustalw not found.\n")

	alignments = dict()
	#with open("infile.pre") as fp:
	for line in f:
		line = line.decode()
		if ' ' in line and not (line.startswith('\n') or line.startswith('PileUp') or line.startswith(' ')):
			name,seq = line.rstrip().split(sep=None,maxsplit=1)
			alignments[name] = alignments.get(name, '') + seq.replace(' ','').replace('.','-')

	'''
	f.seek(0)
	f.truncate()

	f.write(b" ")
	f.write(str.encode(str(len(alignments))))
	f.write(b" ")
	f.write(str.encode(str(len(alignments[name]))))
	f.write(b"\n")
	for i,(name,seq) in enumerate(alignments.items()):
		f.write(b">")
		f.write(str.encode(str(i).ljust(8)))
		f.write(b" ")
		f.write(str.encode(seq))
		f.write(b"\n")

	f.seek(0)
	'''
	text = " "
	text += str(len(alignments))
	text += " "
	text += str(len(alignments[name]))
	text += "\n"
	for i,(name,seq) in enumerate(alignments.items()):
		text += ">"
		text += str(i).ljust(8)
		text += " "
		text += seq
		text += "\n"




	try:
		pipe = Popen(["protdist"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
	except:
		sys.stderr.write("Warning: protdist not found.\n")
	#output = pipe.communicate(input=str.encode(f.name + "\n" + "/dev/stdout"+ "\n" + "Y"))[0]
	output = pipe.communicate(input=text.encode())[0]
	i = 0
	for line in output.decode().split('\n'):
		if line.startswith(">"):
			print(list(alignments.keys())[i], end='\t')
			#print(line)
			print(line.split(sep=None,maxsplit=1)[1])



		
		
		
