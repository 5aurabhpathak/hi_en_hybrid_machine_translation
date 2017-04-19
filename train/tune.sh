#!/bin/bash
#Author: Saurabh Pathak
#tuning script
if [[ $# -ne 2 || $(ps -o stat= -p $$) =~ "+" || ("$1" != "pb" && "$1" != "hpb") ]]
then
	echo "usage: train_tm.sh pb|hpb file_prefix &"
	exit 1
fi

change_absolute () {
	if [ "${1:0:1}" = "/" ]
	then echo $1
	else echo "$PWD/$1"
	fi
}

file=$(change_absolute $2)
ini="$THESISDIR/data/train/truecased/model/$1/moses.ini"
if [ "$1" = "hpb" ]
then
	optmert="-Binarizer 'CreateOnDiskPt 1 1 4 100 2' -Hierarchical"
	decoderopt="-cube-pruning-pop-limit 2000"
else
	optmert=''
	decoderopt="-s 2000 -dl 10"
fi
nohup /opt/moses/scripts/training/mert-moses.pl $file.hi $file.en /opt/moses/bin/moses $ini --working-dir $THESISDIR/data/mert-work/$1/truecased --mertdir /opt/moses/bin --decoder-flags "-threads 16 $decoderopt -v 0" --filterfile "$file.hi $optmert" --threads 16 >& mert$1tc.out
exit 0
