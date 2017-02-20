#!/bin/bash
#Author: Saurabh Pathak
#set of experiments for parameters on PBSMT
#parameters tested: distortion limit
if [[ $# -ne 5 || $(ps -o stat= -p $$) =~ "+" || ($5 != "tuned" && $5 != "untuned") || ($4 != "lowercased" && $4 != "truecased") ]]
then echo "usage: nohup decoder_experiments.sh test_file reference_file outputdir lowercased|truecased tuned|untuned &" && exit 1
fi

change_absolute () {
	if [ "${1:0:1}" = "/" ]
	then echo $1
	else echo "$PWD/$1"
	fi
}

helper() {
	bleu="d$1.bleu"
	if [ ! -s "$bleu" ]
	then
		echo running moses with distortion limit $1 and stack size $3...
		out="translated.d$1.out"
		time moses -dl $1 -s $3 -f $2 -threads 16 -v 0 < $file > $out 2> /dev/null
		$SCRIPTS_ROOTDIR/generic/multi-bleu.perl $ref_file < $out > $bleu
	else echo $bleu exists. Moving on...
	fi
}

test_suite () {
	for dl in {6..15}
	do helper $dl $1 $2
	done
	helper -1 $1 $2
	helper 0 $1 $2
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
mkdir -p pb/$4/$test_dir
cd pb/$4/$test_dir
if [ ! -d "table" ]
then
	$SCRIPTS_ROOTDIR/training/filter-model-given-input.pl table $THESISDIR/data/train/$4/model/pb/moses.ini $file -Binarizer processPhraseTableMin >& /dev/null
	mv table/moses.ini table/moses.untuned.ini
fi
echo Starting $4 tests on $(date)...
a=$(date +%s)
mkdir -p $5/100
cd $5/100
test_suite ../../table/moses.untuned.ini 100
cd ..
for x in {1..4}
do
	stack=$(($x*500))
	mkdir -p $stack && pushd $stack
	test_suite ../../table/moses.untuned.ini $stack
	popd
done
echo Script completed on $(date), took $(duration $a) total.
exit 0
