#!/bin/bash
#Author: Saurabh Pathak
#runs training script
#edit this file to change parameters and train different translation models
#This is to support training of multiple translation models and then batch binarization by binarize_tm.sh.
cd $THESISDIR/data
rm -rf train5/* nohup.out
#imporant export. crashes otherwise.
export PYTHONIOENCODING=utf-8
nohup $SCRIPTS_ROOTDIR/training/train-model.perl -root-dir train5 -corpus corpus/bilingual/parallel/IITB.en-hi.train -f hi -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:5:$PWD/lm/lm.en.5.probing.1.5.blm:8 -external-bin-dir /opt/mgiza/bin -max-phrase-length 5 -mgiza -mgiza-cpus 4 -cores 4 -parallel -sort-buffer-size 2G -sort-batch-size 256 -sort-parallel 4 &
exit 0
