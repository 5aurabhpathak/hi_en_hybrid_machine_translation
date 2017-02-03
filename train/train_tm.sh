#!/bin/bash
#Author: Saurabh Pathak
#runs training script
#edit this file to change parameters and train different translation models
#This is to support training of multiple translation models and then batch binarization by binarize_tm.sh.
rm -rf train/* nohup.out
#imporant export. crashes otherwise.
export PYTHONIOENCODING=utf-8
time nohup /opt/moses/scripts/training/train-model.perl -root-dir train -corpus corpus/bilingual/parallel/IITB.en-hi.clean -f hi -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:4:$HOME/src/python/nlp/mtech-thesis/data/lm/lm.en.4.probing.1.5.blm:8 -external-bin-dir /opt/mgiza/bin -max-phrase-length 5 -mgiza -mgiza-cpus 16 -cores 16 -parallel -sort-buffer-size 10G -sort-batch-size 512 -sort-parallel 16 &
exit 0
