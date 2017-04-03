#!/bin/bash
#Author: Saurabh Pathak
#aligns corpus
function usage {
	echo "usage: nohup align.sh root_dir corpus_stem"
	exit 1
}

if [ $# -ne 2 ]
then usage
fi

change_absolute () {
	if [ "${1:0:1}" = "/" ]
	then echo $1
	else echo "$PWD/$1"
	fi
}

mkdir -p $1
OUT_DIR=$(change_absolute $1)
IN_DIR=$(change_absolute $2)
#imporant export. crashes otherwise.
export PYTHONIOENCODING=utf-8
$SCRIPTS_ROOTDIR/training/train-model.perl -root-dir $OUT_DIR -corpus $IN_DIR -f hi -e en -alignment grow-diag-final-and --last-step 3 -external-bin-dir /opt/mgiza/bin -mgiza -mgiza-cpus 4 -cores 4 -parallel -sort-buffer-size 2G -sort-batch-size 256 -sort-parallel 4
exit 0
