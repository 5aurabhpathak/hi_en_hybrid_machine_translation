#!/bin/bash
#Author: Saurabh Pathak
#creates csv from experiments results and makes graphs
cd $THESISDIR/data/results/

function to_minutes {
	min=$(cut -dm -f1 <<< $1)
	sec=$(cut -dm -f2 <<< $1 | cut -ds -f1)
	awk 'BEGIN {print '$min'+'$sec'/60 }'
}

function csv {
	echo $stack 0 $(cat $stack/d0.bleu | cut -d, -f1 | cut -d' ' -f3) $(to_minutes ${timearray[$i]}) >> $bleu
	i=$(($i+1))
	for z in $(seq 6 12)
	do
		echo $stack $z $(cat $stack/d$z.bleu | cut -d, -f1 | cut -d' ' -f3) $(to_minutes ${timearray[$i]}) >> $bleu
		i=$(($i+1))
	done
	echo $stack -1 $(cat $stack/d-1.bleu | cut -d, -f1 | cut -d' ' -f3) $(to_minutes ${timearray[$i]}) >> $bleu
	i=$(($i+1))
}

for x in truecased lowercased
do
	for y in untuned tuned
	do
		pushd pb/$x/test/$y >& /dev/null
		bleu="$PWD/bleu.csv"
		declare -a timearray
		timearray=($(cat "$THESISDIR/data/pb"$x"tests$y.out" | grep real | cut -f2))
		stack=100
		i=0
		> $bleu
		csv
		for stack in $(seq 500 500 2000)
		do csv
		done
		$THESISDIR/test/visualise_pbresults.py --input $bleu
		popd >& /dev/null
	done
done
for x in truecased lowercased
do
	for y in untuned tuned
	do
		pushd hpb/$x/test/$y >& /dev/null
		bleu="$PWD/bleu.csv"
		declare -a timearray
		timearray=($(cat "$THESISDIR/data/hpb"$x"tests$y.out" | grep real | cut -f2))
		i=0
		> $bleu
		for z in $(seq 500 500 2500)
		do
			echo $z $(cat l$z.bleu | cut -d, -f1 | cut -d' ' -f3) $(to_minutes ${timearray[$i]}) >> $bleu
			i=$(($i+1))
		done
		$THESISDIR/test/visualise_hpbresults.py --input $bleu
		popd >& /dev/null
	done
done
exit 0
