#!/bin/bash
#Author: Saurabh Pathak
#Step 1
#training of language model -- run this multiple times with different order arguments if you want to create more than one language models
#requires moses installed and moses/bin in $PATH
#long process - you may want to alter priority of the process.
cd $THESISDIR/data
if [ $# -ne 3 ]
then echo 'Usage: train_lm.sh n-gram-order text arpa' && exit 1
fi
nohup lmplz -o $1 -T . --text $2 --arpa $3 &
exit 0
