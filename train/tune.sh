#!/bin/bash
#Author: Saurabh Pathak
rm -rf mert-work/* nohup.out
nohup /opt/moses/scripts/training/mert-moses.pl corpus/bilingual/dev_test_tokenized/dev.true.hi corpus/bilingual/dev_test_tokenized/dev.true.en /opt/moses/bin/moses train/model/moses.ini --mertdir /opt/moses/bin --decoder-flags '-threads 16' --mertargs '--threads 16' &
exit 0
