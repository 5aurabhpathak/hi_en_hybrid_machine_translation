#!/bin/bash
#Author: Saurabh Pathak
#First step
#downloads and extracts the corpora
#corpus downloaded: www.statmt.org/lm-benchmark (4.3 GB uncompressed, 32.1M senetences, 1B < vocabulary size!) and IITB Hindi-English Parallel corpus (1.5M pair of senetences)
cd $HOME/src/python/nlp/mtech-thesis/data/downloaded_corpora
echo Downloading monolingual data...
wget -nc http://www.statmt.org/lm-benchmark/1-billion-word-language-modeling-benchmark-r13output.tar.gz
echo -n Extracting...
mkdir -p ../corpus/monolingual
tar -C ../corpus/monolingual -zxf 1-billion-word-language-modeling-benchmark-r13output.tar.gz 1-billion-word-language-modeling-benchmark-r13output/training-monolingual.tokenized.shuffled 1-billion-word-language-modeling-benchmark-r13output/heldout-monolingual.tokenized.shuffled/news.en-00000-of-00100 --strip-components 2
echo done.
echo Downloading bilingual data...
wget -nc --user=wat2016 --ask-password http://www.cfilt.iitb.ac.in/iitb_parallel/iitb_corpus_download/parallel.tgz
wget -nc --user=wat2016 --ask-password http://www.cfilt.iitb.ac.in/iitb_parallel/iitb_corpus_download/dev_test_tokenized.tgz
echo -n Extracting...
mkdir -p ../corpus/bilingual
tar -zxf parallel.tgz -C ../corpus/bilingual
tar -zxf dev_test_tokenized.tgz -C ../corpus/bilingual
cd ../corpus/bilingual/parallel
#to reflect corpus status - both already tokenized and no need to truecase hindi
mv IITB.en-hi.en IITB.en-hi.tok.en
mv IITB.en-hi.hi IITB.en-hi.true.hi
cd ../dev_test_tokenized
mv dev.en dev.tok.en
mv dev.hi dev.true.hi
mv test.en test.tok.en
mv test.hi test.true.hi
echo done.
cd ../../monolingual
#monolingual data needs merging of various files into one big file, also including english sentences from parallel corpora
echo -n merging monolingual files...
for x in $(ls -1)
do
	cat $x >> monolingual.tok.en
	rm -f $x
done
cat ../bilingual/parallel/IITB.en-hi.tok.en >> monolingual.tok.en
echo done.
exit 0
