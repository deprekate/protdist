# Makefile
#
# Unix Makefile for PHYLIP 3.695

PACKAGE=phylip
VERSION=3.695

CC      = gcc
CFLAGS  = -g
LIBS    = -lm

all:	protdist

phylip.o:     phylip.h
seq.o:        phylip.h seq.h
protdist.o:   protdist.c seq.h phylip.h

protdist:  protdist.o seq.o phylip.o
	$(CC) $(CFLAGS) protdist.o seq.o phylip.o $(LIBS) -o protdist



.PHONY: clean
clean:
	@rm -f *.o
	@rm -f protdist

# Makefile
