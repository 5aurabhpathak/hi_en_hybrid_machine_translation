#!/bin/bash
#Author: Saurabh Pathak
#Runs meteor and produces final score
#first argument is outputfile second is reference file
change_absolute () {
	if [ "${1:0:1}" = "/" ]
	then echo $1
	else echo "$PWD/$1"
	fi
}

IN="$(change_absolute $1)"
OUT="$(change_absolute $2)"

cd $THESISDIR/data/downloaded/meteor-1.5
java -Xmx2G -jar meteor-1.5.jar $IN $OUT -l en -q 2>/dev/null
exit 0
