#!/bin/bash
#Author: Saurabh Pathak
#Step 1
#training of language model -- run this multiple times with different order arguments if you want to create more than one language models
#requires moses installed and moses/bin in $PATH
#long process - run with sudo if you want to alter priority of the process
cd $HOME/src/python/nlp/mtech-thesis/data
nohup lmplz -o $1 -T . --text monolingual/monolingual.true.en --arpa lm/lm.en.$1.arpa &
x=$(pgrep lmplz)
if [ $# -ne 1 ]
then
	echo 'Usage: ./train_lm.sh [n-gram order]'
fi
if [ $UID -eq 0 ] #sudo
then
	renice -n -5 -p $x
	ionice -c 1 -n 0 -p $x
fi
echo "Started training process in background with pid $x. Please wait until it finishes. Check nohup.out for status (tail --follow nohup.out) . You can close this terminal now if you wish."
exit 0
