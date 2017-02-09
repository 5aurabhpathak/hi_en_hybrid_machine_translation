#!/bin/bash
#Author: Saurabh Pathak
#Second step
#performs casing on monolingual as well as parallel corpus (english part)
#uses perl scripts provided with moses
#Run after - 'download_corpora.sh'
#Requires - Monolingual Corpus and Parallel Corpus in respective directories
echo Generating truecase model...
cd $THESISDIR/data/corpus/monolingual
time $SCRIPTS_ROOTDIR/recaser/train-truecaser.perl --model ../truecase-model.en --corpus monolingual.tok.en
echo truecasing monolingual corpus...
time $SCRIPTS_ROOTDIR/recaser/truecase.perl --model ../truecase-model.en < monolingual.tok.en > monolingual.true.en
echo lowercasing monolingual corpus...
#necessary for training lc language models
time $SCRIPTS_ROOTDIR/tokenizer/lowercase.perl < monolingual.tok.en > monolingual.lc.en
cd ../bilingual/parallel
#lowercasing will be performed after the training sets are generated in separate.sh. No need to do so now.
echo truecasing english side of bilingual corpus...
time $SCRIPTS_ROOTDIR/recaser/truecase.perl --model ../../truecase-model.en < IITB.en-hi.tok.en > IITB.en-hi.true.en
echo processing english side of test and development sets
cd ../dev_test_tokenized
echo truecasing dev set...
time $SCRIPTS_ROOTDIR/recaser/truecase.perl --model ../../truecase-model.en < dev.tok.en > dev.true.en
echo truecasing dev set...
time $SCRIPTS_ROOTDIR/recaser/truecase.perl --model ../../truecase-model.en < test.tok.en > test.true.en
echo done.
exit 0
