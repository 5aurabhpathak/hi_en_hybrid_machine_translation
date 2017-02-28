#!/bin/bash
#Author: Saurabh Pathak
#set of experiments for parameters on HPBSMT
#parameters tested: cube-pruning-pop-limit
if [[ $# -ne 5 || $(ps -o stat= -p $$) =~ "+" || ("$5" != "tuned" && "$5" != "untuned") || ("$4" != "lowercased" && "$4" != "truecased") ]]
then echo "usage: nohup decoder_experiments.sh test_file reference_file outputdir lowercased|truecased tuned|untuned &" && exit 1
fi

change_absolute () {
	if [ "${1:0:1}" = "/" ]
	then echo $1
	else echo "$PWD/$1"
	fi
}

helper() {
	bleu="l$2.bleu"
	if [ ! -s "$bleu" ]
	then
		echo running moses with cube-pruning-pop-limit $2...
		out="translated.l$2.out"
		time moses -cube-pruning-pop-limit $2 -f $1 -threads 16 -v 0 < $file > $out 2> /dev/null
		$SCRIPTS_ROOTDIR/generic/multi-bleu.perl $ref_file < $out > $bleu
	else echo $bleu exists. Moving on...
	fi
}

test_suite () {
	for x in {1..5}
	do
		cppl=$(($x*500))
		helper $1 $cppl
	done
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
output_dir=$(change_absolute $3)
test_dir=$(echo $file | grep -o '[^/]*$' | cut -d. -f1-2)
mkdir -p $output_dir
cd $output_dir
mkdir -p hpb/$4/$test_dir
cd hpb/$4/$test_dir
if [ "$5" = "untuned" ]
then ini="$THESISDIR/data/train/$4/model/hpb/moses.ini"
else ini="$THESISDIR/data/mert-work/hpb/moses.ini"
fi
if [ ! -d "table" ]
then
	$SCRIPTS_ROOTDIR/training/filter-model-given-input.pl table $ini $file -Binarizer 'CreateOnDiskPt 1 1 4 100 2' -Hierarchical >& /dev/null
	mv table/moses.ini table/moses.$5.ini
	rm table/phrase-table.0-0.1.1 info input.*
else $SCRIPTS_ROOTDIR/ems/support/substitute-filtered-tables.perl table/moses.* < $ini > table/moses.$5.ini
fi
echo Starting $4 tests on $(date)...
a=$(date +%s)
mkdir -p $5
cd $5
test_suite ../table/moses.$5.ini
echo Script completed on $(date), took $(duration $a) total.
exit 0
