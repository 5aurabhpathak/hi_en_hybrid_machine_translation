#!/bin/bash
#Author: Saurabh Pathak
#set of experiments for parameters
#parameters tested: distortion limit and stack size
if [[ $# -ne 2 || $(ps -o stat= -p $$) =~ "+" ]]
then
	echo "usage: nohup decoder_experiments.sh test_file reference_file &"
	exit 1
fi

change_absolute () {
	if [ "${1:0:1}" = "/" ]
	then echo $1
	else echo "$PWD/$1"
	fi
}

helper() {
	curbig=0
	for x in {1..15}
	do
		s=$(($x*100))
		bleu="s$s.d$1.bleu"
		if [ ! -f "$bleu" ]
		then
			echo running moses with distortion limit $1 and stack size $s...
			out="translated.s$s.d$1.out"
			time moses -dl $1 -s $s -f table/moses.ini < $file > $out 2> /dev/null
			$SCRIPTS_ROOTDIR/generic/multi-bleu.perl $ref_file < $out > $bleu
		else echo $bleu exists. Moving on...
		fi
		cur=$(cat $bleu | cut -d, -f1 | cut -d' ' -f3)
		curbig=$(echo $curbig $cur | awk '{if($1 < $2) print $2; else print $1}')
	done
}

test_suite () {
	if [ ! -d "table" ]
	then $SCRIPTS_ROOTDIR/training/filter-model-given-input.pl table $1 $file -Binarizer processPhraseTableMin >& /dev/null
	fi
	biggest=0
	flag=0
	for dl in {6..14}
	do
		helper $dl
		if [ 1 -eq $(echo $curbig $biggest | awk '{if($1 < $2) print 1; else print 0}') ]
		then if [ flag -eq 1 ]
		then echo none of the scores obtained with dl $dl were bigger than previous dl step. Stopping here. && break
		else flag=1
		fi
		else biggest=$curbig
		fi
	done
	helper -1
	helper 0
}

duration() {
	sec=$(($(date +%s)-$1))
	echo -n "$(($sec/86400)) days "
	sec=$(($sec%86400))
	echo -n "$(($sec/3600)) hours "
	sec=$(($sec%3600))
	echo -n "$(($sec/60)) minutes $(($sec%60)) seconds "
}

file=$(change_absolute $1)
ref_file=$(change_absolute $2)
output_dir=$(echo $file | grep -o '[^/]*$' | cut -d. -f1-2)
cd $THESISDIR/data/results
echo Starting tests on untuned moses.ini on $(date)...
a=$(date +%s)
mkdir -p $output_dir/untuned
cd $output_dir/untuned
test_suite ../../../train/model/moses.ini
echo finished. Took $(duration $a) to complete.

echo Starting tests on tuned moses.ini on $(date)...
if [ ! -f ../../../mert-work ]
then echo tuned moses.ini not found. Skipping.
else
	b=$(date +%s)
	mkdir -p ../tuned
	cd ../tuned
	test_suite ../../../mert-work/moses.ini
	echo finished. Took $(duration $b) to complete.
fi
echo Script completed on $(date), took $(duration $a) total.
exit 0
