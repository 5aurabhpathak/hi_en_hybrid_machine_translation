#!/bin/bash
#Author: Saurabh Pathak
#decoding with post decoding transliteration
if [ $# -ne 2 ]
then
	echo usage: decode.sh inputfile outputfile
	exit 1
fi

cd $THESISDIR/data
moses -f train/model/moses.ini -threads 16 -output-unknowns oov -v 0 < $1 > $2
exit 0
