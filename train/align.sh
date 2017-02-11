#!/bin/bash
#Author: Saurabh Pathak
#runs training script
#edit this file to change parameters and train different translation models
#This is to support training of multiple translation models and then batch binarization by binarize_tm.sh.
if [[ $# -ne 2 || $(ps -o stat= -p $$) =~ "+" ]]
then
	echo "usage: nohup train_tm.sh root_dir corpus_stem &"
	exit 1
fi

cd $THESISDIR/data
rm -rf $1
mkdir -p $1
#imporant export. crashes otherwise.
export PYTHONIOENCODING=utf-8
$SCRIPTS_ROOTDIR/training/train-model.perl -root-dir $1 -corpus $2 -f hi -e en -alignment grow-diag-final-and --last-step 3 -external-bin-dir /opt/mgiza/bin -mgiza -mgiza-cpus 16 -cores 16 -parallel -sort-buffer-size 10G -sort-batch-size 512 -sort-parallel 16
exit 0
