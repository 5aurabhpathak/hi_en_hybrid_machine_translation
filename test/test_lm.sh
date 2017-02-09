#!/bin/bash
#Author: Saurabh Pathak
#Comparison of the language models that have been trained.
function test_suite {
	if [[ $1 =~ "lc" ]]
	then y=lc
	else y=true
	fi
	for x in $(ls -1 $1 | grep blm)
	do
		echo using language model $x...
		query $1/$x < corpus/bilingual/dev_test_tokenized/test.$y.en >tmp 2>tmp.err
		cat tmp | grep -i perplexity
		echo query time:
		cat tmp.err
		rm -f tmp tmp.err
	done
}

cd $THESISDIR/data
echo testing truecased models...
test_suite lm
echo testing lowercased models...
test_suite lm/lc
exit 0
