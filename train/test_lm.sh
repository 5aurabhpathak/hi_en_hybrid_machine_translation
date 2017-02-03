#!/bin/bash
#Author: Saurabh Pathak
#Comparison of the language models that have been trained.
cd $HOME/src/python/nlp/mtech-thesis/data
for x in $(ls -1 lm | grep blm)
do
	echo using language model $x...
	/opt/moses/bin/query lm/$x < test_lm_sents.txt >tmp 2>tmp.err
	cat tmp | grep -i perplexity
	echo query time: $(cat tmp.err | tail -n 1 | grep -o '[^:]*$')
	rm -f tmp tmp.err
done
