#!/bin/bash
#Author: Saurabh Pathak
#binarize the language models created with step 1
#Step 2
#uses default arguments (Probing table 1.5 ratio)
if [[ $(ps -o stat= -p $$) =~ "+" ]]
then
	echo "usage: [nohup] binarize_lm.sh &"
	exit 1
fi

function binarize {
	cd $1
	for x in $(ls -1 | grep blm)
	do build_binary -T . $x $(echo $x | grep -o '^.*\.')probing.1.5.blm &
	done
	cd -
}

cd $THESISDIR/data
binarize lm/
binarize lm/lc
exit 0
